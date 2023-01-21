import { useEffect, useState } from "react";
import Chamber from "./Chamber";
import { ReactComponent as Fan } from "../assets/fan.svg";

const ws = new WebSocket(
  `ws://${import.meta.env.VITE_SERVER_URL}:${import.meta.env.VITE_SERVER_PORT}`
);

function sendHumidity(humidity: Number) {
  const humidityEvent = {
    type: "humidity",
    value: humidity,
  };
  ws.send(JSON.stringify(humidityEvent));
}

function sendTemperature(temperature: Number) {
  const temperatureEvent = {
    type: "temperature",
    value: temperature,
  };
  ws.send(JSON.stringify(temperatureEvent));
}

export default function MainPage() {
  const [currentTemperature, setCurrentTemperature] = useState(0);
  const [targetTemperature, setTargetTemperature] = useState(0);
  const [currentHumidity, setCurrentHumidity] = useState(0);
  const [targetHumidity, setTargetHumidity] = useState(0);
  const [fanSpeed, setFanSpeed] = useState(0);

  useEffect(() => {
    ws.onmessage = (ev) => {
      if (typeof ev.data === "string") {
        const event = JSON.parse(ev.data);
        switch (event.type) {
          case "temperature":
            setCurrentTemperature(event.value);
            break;
          case "humidity":
            setCurrentHumidity(event.value);
            break;
          default:
            console.log(`Failed to parse event ${JSON.stringify(event)}`);
        }
      }
    };
  }, [ws, setCurrentTemperature, setCurrentHumidity]);

  return (
    <div className="flex w-screen h-screen py-16">
      <Chamber
        currentTemperature={currentTemperature}
        targetTemperature={targetTemperature}
        setTargetTemperature={(temperature) => {
          setTargetTemperature(temperature);
          sendTemperature(temperature);
        }}
        currentHumidity={currentHumidity}
        targetHumidity={targetHumidity}
        setTargetHumidity={(humidity) => {
          setTargetHumidity(humidity);
          sendHumidity(humidity);
        }}
        className="w-full h-full"
      />
      <div className="mx-8 h-full w-min">
        <Fan className="w-full h-min mx-auto fill-white" />
        <div className="py-8 mt-4 border-4 h-full border-slate-600">
          <input
            type="range"
            min={0}
            max={3}
            step={1}
            value={fanSpeed}
            onChange={(ev) => setFanSpeed(parseInt(ev.target.value))}
            className="fan-slider h-full"
          />
        </div>
      </div>
      <Chamber
        currentTemperature={currentTemperature}
        targetTemperature={targetTemperature}
        setTargetTemperature={setTargetTemperature}
        currentHumidity={currentHumidity}
        targetHumidity={targetHumidity}
        setTargetHumidity={setTargetHumidity}
        className="w-full h-full"
      />
    </div>
  );
}
