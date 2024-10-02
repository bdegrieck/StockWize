import Image from "next/image";
import BrainLight from "@/app/assets/images/BrainLight.png";

export default function BrainLightLogo() {
    return (
        <Image
        src={BrainLight}
        alt="Brain"
        height={250}
        width={250}
      /> 
    )
}