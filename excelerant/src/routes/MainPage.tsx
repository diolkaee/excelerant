import { useState } from "react";
import { ReactComponent as Fan } from "../assets/fan.svg";
import { ReactComponent as Logo } from "../assets/logo.svg";
import { ExposureRange, useExcelerant } from "../hooks/useExcelerant";
import Chamber from "../components/Chamber";

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
    <div className="flex w-screen h-screen bg-black py-16">
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
      <div className="flex flex-col justify-evenly mx-8 h-full w-min">
        <Logo className="w-40 h-40 mx-auto" />
        <div className="mx-auto py-8 mt-12 rounded-xl border-4 h-full border-excelerant">
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
