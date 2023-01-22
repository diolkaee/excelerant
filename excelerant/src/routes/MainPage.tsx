import { useState } from "react";
import { ReactComponent as Fan } from "../assets/fan.svg";
import { useExcelerant } from "../hooks/useExcelerant";
import Chamber from "./Chamber";

export default function MainPage() {
  const [growTargetTemperature, setGrowTargetTemperature] = useState(0);
  const [growTargetHumidity, setGrowTargetHumidity] = useState(0);
  const [bloomTargetTemperature, setBloomTargetTemperature] = useState(0);
  const [bloomTargetHumidity, setBloomTargetHumidity] = useState(0);
  const [targetFanSpeed, setTargetFanSpeed] = useState(0);

  const {
    growTemperature,
    sendGrowTemperature,
    bloomTemperature,
    sendBloomTemperature,
    growHumidity,
    sendGrowHumidity,
    bloomHumidity,
    sendBloomHumidity,
    growPower,
    sendGrowPower,
    bloomPower,
    sendBloomPower,
    fanSpeed,
    sendFanSpeed,
  } = useExcelerant();

  return (
    <div className="flex w-screen h-screen bg-black py-16">
      <Chamber
        hasPower={growPower}
        setHasPower={sendGrowPower}
        currentTemperature={growTemperature}
        targetTemperature={growTargetTemperature}
        setTargetTemperature={(temperature) => {
          setGrowTargetTemperature(temperature);
          sendGrowTemperature(temperature);
        }}
        currentHumidity={growHumidity}
        targetHumidity={growTargetHumidity}
        setTargetHumidity={(humidity) => {
          setGrowTargetHumidity(humidity);
          sendGrowHumidity(humidity);
        }}
        className="w-full h-full"
      />
      <div className="mx-8 h-full w-min">
        <Fan className="w-full h-min mx-auto fill-white" />
        <div className="py-8 mt-4 border-4 h-2/3 border-slate-600">
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
            className="fan-slider h-full"
          />
        </div>
      </div>
      <Chamber
        hasPower={bloomPower}
        setHasPower={sendBloomPower}
        currentTemperature={bloomTemperature}
        targetTemperature={bloomTargetTemperature}
        setTargetTemperature={(temperature) => {
          setBloomTargetTemperature(temperature);
          sendBloomTemperature(temperature);
        }}
        currentHumidity={bloomHumidity}
        targetHumidity={bloomTargetHumidity}
        setTargetHumidity={(humidity) => {
          setBloomTargetHumidity(humidity);
          sendBloomHumidity(humidity);
        }}
        className="w-full h-full"
      />
    </div>
  );
}
