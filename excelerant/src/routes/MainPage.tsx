import { useState } from "react";
import { ReactComponent as Fan } from "../assets/fan.svg";
import { ReactComponent as Logo } from "../assets/logo.svg";
import Chamber from "../components/Chamber";
import { ExposureRange, useExcelerant } from "../hooks/useExcelerant";

export default function MainPage() {
  const [targetFanSpeed, setTargetFanSpeed] = useState(0);
  const [targetGrowExposure, setTargetGrowExposure] = useState<ExposureRange>({
    start: { hour: 1, minute: 1 },
    duration: { hour: 2, minute: 2 },
  });
  const [targetBloomExposure, setTargetBloomExposure] = useState<ExposureRange>(
    {
      start: { hour: 0, minute: 0 },
      duration: { hour: 0, minute: 0 },
    }
  );

  const {
    growTemperature,
    bloomTemperature,
    growHumidity,
    bloomHumidity,
    sendGrowExposure,
    sendBloomExposure,
    growPower,
    sendGrowPower,
    bloomPower,
    sendBloomPower,
    sendFanSpeed,
  } = useExcelerant();

  return (
    <div className="flex w-screen h-screen bg-black py-8 lg:py-16">
      <Chamber
        hasPower={growPower}
        setHasPower={sendGrowPower}
        currentTemperature={growTemperature}
        currentHumidity={growHumidity}
        exposure={targetGrowExposure}
        setExposure={(exposure) => {
          setTargetGrowExposure(exposure);
          sendGrowExposure(exposure);
        }}
        className="w-full h-full"
      />
      <div className="flex flex-col justify-evenly sm:mx-4 lg:mx-8 h-full w-min">
        <Logo className="h-20 lg:h-40 mx-auto" />
        <div className="flex flex-col items-center mx-auto px-4 py-8 mt-12 rounded-xl border-4 h-full w-min border-excelerant">
          <input
            type="range"
            min={0}
            max={9}
            step={1}
            value={targetFanSpeed}
            onChange={(ev) => {
              const fanSpeed = parseInt(ev.target.value);
              setTargetFanSpeed(fanSpeed);
              sendFanSpeed(fanSpeed);
            }}
            orient="vertical"
            className="fan-slider h-5/6 accent-excelerant"
          />
          <Fan className="w-14 h-14 mt-8 mx-auto fill-crystalwhite" />
        </div>
      </div>
      <Chamber
        hasPower={bloomPower}
        setHasPower={sendBloomPower}
        currentTemperature={bloomTemperature}
        currentHumidity={bloomHumidity}
        exposure={targetBloomExposure}
        setExposure={(exposure) => {
          setTargetBloomExposure(exposure);
          sendBloomExposure(exposure);
        }}
        className="w-full h-full"
      />
    </div>
  );
}
