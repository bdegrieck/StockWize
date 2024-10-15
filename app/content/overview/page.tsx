import { TextBox, TextBoxContainer } from "@/app/components/TextBox";

export default function Overview() {
    return (
        <div className="container-fluid h-100 d-flex flex-column gap-3">
            <TextBoxContainer>
                <TextBox title="52 Week High" body="$236.96" centerText={true} />
                <TextBox title="52 Week Low" body="$163.67" centerText={true}/>
                <TextBox title="Market Cap" body="3,357,369,434,000.00" centerText={true} />
            </TextBoxContainer>
            <TextBox title="Company Description" body="Apple Inc. is an American multinational corporation and technology companyincorporated and headquartered in Cupertino, California, in Silicon Valley.[1] It is best known for its consumer electronics, software, and services. The company was incorporated as Apple Computer, Inc. by Steve Wozniak and Steve Jobs in 1977; as of 2023, Apple is the largest technology company by revenue, with US$394.33 billion"/>
        </div>
    );
}