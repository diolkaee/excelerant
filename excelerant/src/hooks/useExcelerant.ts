import { useCallback, useContext, useEffect, useState } from "react";
import { ExcelerantContext } from "../contexts/ExcelerantContext";

type ExcelerantChamber = "grow" | "bloom";
type ExcelerantEvent = "temperature" | "humidity" | "fanSpeed" | "power";

function sendEvent<T>(
  websocket: WebSocket,
  eventType: ExcelerantEvent,
  eventValue: T,
  chamber?: ExcelerantChamber
) {
  const event = {
    chamber: chamber,
    type: eventType,
    value: eventValue,
  };
  websocket.send(JSON.stringify(event));
}

export function useExcelerant(): {
  growTemperature: number;
  sendGrowTemperature: (temperature: Number) => void;
  bloomTemperature: number;
  sendBloomTemperature: (temperature: Number) => void;
  growHumidity: number;
  sendGrowHumidity: (humidity: Number) => void;
  bloomHumidity: number;
  sendBloomHumidity: (humidity: Number) => void;
  growPower: boolean;
  sendGrowPower: (hasPower: boolean) => void;
  bloomPower: boolean;
  sendBloomPower: (hasPower: boolean) => void;
  fanSpeed: number;
  sendFanSpeed: (fanSpeed: Number) => void;
} {
  const excelerant = useContext(ExcelerantContext);
  const [growTemperature, setGrowTemperature] = useState(0);
  const [bloomTemperature, setBloomTemperature] = useState(0);
  const [growHumidity, setGrowHumidity] = useState(0);
  const [bloomHumidity, setBloomHumidity] = useState(0);
  const [growPower, setGrowPower] = useState(false);
  const [bloomPower, setBloomPower] = useState(false);
  const [fanSpeed, setFanSpeed] = useState(0);

  useEffect(() => {
    excelerant.onmessage = (ev) => {
      const event = JSON.parse(ev.data);
      const chamber = event.chamber as ExcelerantChamber | undefined;
      switch (event.type) {
        case "temperature":
          chamber === "grow"
            ? setGrowTemperature(event.value)
            : setBloomTemperature(event.value);
          break;
        case "humidity":
          chamber === "grow"
            ? setGrowHumidity(event.value)
            : setBloomHumidity(event.value);
          break;
        case "power":
          chamber === "grow"
            ? setGrowPower(event.value)
            : setBloomPower(event.value);
          break;
        case "fanspeed":
          setFanSpeed(event.value);
        default:
          console.log(`Failed to parse event ${JSON.stringify(event)}`);
      }
    };
  }, [excelerant]);

  const sendGrowTemperature = useCallback(
    (temperature: Number) =>
      sendEvent(excelerant, "temperature", temperature, "grow"),
    [excelerant]
  );

  const sendBloomTemperature = useCallback(
    (temperature: Number) =>
      sendEvent(excelerant, "temperature", temperature, "bloom"),
    [excelerant]
  );

  const sendGrowHumidity = useCallback(
    (humidity: Number) => sendEvent(excelerant, "humidity", humidity, "grow"),
    [excelerant]
  );

  const sendBloomHumidity = useCallback(
    (humidity: Number) => sendEvent(excelerant, "humidity", humidity, "bloom"),
    [excelerant]
  );

  const sendGrowPower = useCallback(
    (hasPower: boolean) => sendEvent(excelerant, "power", hasPower, "grow"),
    [excelerant]
  );

  const sendBloomPower = useCallback(
    (hasPower: boolean) => sendEvent(excelerant, "power", hasPower, "bloom"),
    [excelerant]
  );

  const sendFanSpeed = useCallback(
    (fanSpeed: Number) => sendEvent(excelerant, "fanSpeed", fanSpeed),
    [excelerant]
  );

  return {
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
  };
}
