from typing import Dict

import pandas as pd
import torch
from pytorch_forecasting import AutoRegressiveBaseModel, LSTM, TimeSeriesDataSet
from torch import nn

from BackEnd.Models.arima import ForecastField


class LSTMModel(AutoRegressiveBaseModel):
    def __init__(
        self,
        target: str,
        target_lags: Dict[str, Dict[str, int]],
        n_layers: int,
        hidden_size: int,
        input_size: int,
        dropout: float = 0.1,
        **kwargs,
    ):
        """
        Args:
            target: Target column
            target_lags: Lags for each target
            input_size: number of features
            n_layers: Number of layers in the model
            hidden_size: Output size of each neuron cell. Higher value the more complexity
            dropout: Percent of units being dropped during training
            **kwargs:
        """
        self.save_hyperparameters()
        super().__init__(**kwargs)

        self.lstm = LSTM(
            hidden_size=self.hparams.hidden_size,
            input_size=self.hparams.input_size,
            num_layers=self.hparams.n_layers,
            dropout=self.hparams.dropout,
            batch_first=True,
        )
        self.output_layer = nn.Linear(self.hparams.hidden_size, out_features=1)

    def encode(self, x: Dict[str, torch.Tensor]) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x: Input features for the lstm encoded
        Returns:
            A tuple of the hidden state [0] and the cell state [1]
        """
        input_vector = x["encoder_cont"].clone()
        input_vector[..., self.target_positions] = torch.roll(
            input_vector[..., self.target_positions], shifts=1, dims=1
        )
        input_vector = input_vector[:, 1:]
        effective_encoder_lengths = x["encoder_lengths"] - 1
        _, hidden_state = self.lstm(
            input_vector, lengths=effective_encoder_lengths, enforce_sorted=False  # passing the lengths directly
        )  # second ouput is not needed (hidden state)
        return hidden_state

    def decode(self, x: Dict[str, torch.Tensor], hidden_state):
        input_vector = x["decoder_cont"].clone()
        input_vector[..., self.target_positions] = torch.roll(
            input_vector[..., self.target_positions], shifts=1, dims=1
        )
        # but this time fill in missing target from encoder_cont at the first time step instead of throwing it away
        last_encoder_target = x["encoder_cont"][
            torch.arange(x["encoder_cont"].size(0), device=x["encoder_cont"].device),
            x["encoder_lengths"] - 1,
            self.target_positions.unsqueeze(-1),
        ].T
        input_vector[:, 0, self.target_positions] = last_encoder_target

        if self.training:  # training mode
            lstm_output, _ = self.lstm(input_vector, hidden_state, lengths=x["decoder_lengths"], enforce_sorted=False)

            # transform into right shape
            prediction = self.output_layer(lstm_output)
            prediction = self.transform_output(prediction, target_scale=x["target_scale"])

            # predictions are not yet rescaled
            return prediction

        else:  # prediction mode
            target_pos = self.target_positions

            def decode_one(idx, lagged_targets, hidden_state):
                x = input_vector[:, [idx]]
                # overwrite at target positions
                x[:, 0, target_pos] = lagged_targets[-1]  # take most recent target (i.e. lag=1)
                lstm_output, hidden_state = self.lstm(x, hidden_state)
                # transform into right shape
                prediction = self.output_layer(lstm_output)[:, 0]  # take first timestep
                return prediction, hidden_state

            # make predictions which are fed into next step
            output = self.decode_autoregressive(
                decode_one,
                first_target=input_vector[:, 0, target_pos],
                first_hidden_state=hidden_state,
                target_scale=x["target_scale"],
                n_decoder_steps=input_vector.size(1),
            )

            # predictions are already rescaled
            return output


    def forward(self, dataset: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        data_loader = dataset.to_dataloader()
        x, y = next(iter(data_loader))
        hidden_state = self.encode(x)  # encode to hidden state
        output = self.decode(x, hidden_state)  # decode leveraging hidden state

        return self.to_network_output(prediction=output)

def convert_df(
        df: pd.DataFrame,
        time_idx: str,
        target: str,
        grouped_dim: list[str],
        steps: ForecastField,
        known_cat_vars: list[str],
        unknown_cont_vars: list[str]
):
    data = TimeSeriesDataSet(
        data=df,
        time_idx=time_idx,
        target=target,
        group_ids=grouped_dim,
        # max_encoder_length=None,
        max_prediction_length=steps.days,
        static_categoricals=known_cat_vars,
        time_varying_unknown_reals=unknown_cont_vars,
        predict_mode=True,
    )
    return data
