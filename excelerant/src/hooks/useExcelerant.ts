import { useCallback, useContext, useEffect, useState } from "react";
import { ExcelerantContext } from "../contexts/ExcelerantContext";

type ExcelerantChamber = "grow" | "bloom";
type ExcelerantEvent =
  | "temperature"
  | "humidity"
  | "fanSpeed"
  | "exposure"
  | "power";
export type Time = { hour: number; minute: number };
export type ExposureRange = { start: Time; duration: Time };

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
  bloomTemperature: number;
  growHumidity: number;
  bloomHumidity: number;
  growExposure: ExposureRange;
  sendGrowExposure: (exposure: ExposureRange) => void;
  bloomExposure: ExposureRange;
  sendBloomExposure: (exposure: ExposureRange) => void;
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
  const [growExposure, setGrowExposure] = useState<ExposureRange>({
    start: {
      hour: 0,
      minute: 0,
    },
    duration: {
      hour: 0,
      minute: 0,
    },
  });
  const [bloomExposure, setBloomExposure] = useState<ExposureRange>({
    start: {
      hour: 0,
      minute: 0,
    },
    duration: {
      hour: 0,
      minute: 0,
    },
  });

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
        case "exposure":
          chamber === "grow"
            ? setGrowExposure(event.value)
            : setBloomExposure(event.value);
          break;
        case "fanspeed":
          setFanSpeed(event.value);
          break;
        default:
          console.log(`Failed to parse event ${JSON.stringify(event)}`);
      }
    };
  }, [excelerant]);

  const sendGrowPower = useCallback(
    (hasPower: boolean) => sendEvent(excelerant, "power", hasPower, "grow"),
    [excelerant]
  );

  const sendBloomPower = useCallback(
    (hasPower: boolean) => sendEvent(excelerant, "power", hasPower, "bloom"),
    [excelerant]
  );

  const sendGrowExposure = useCallback(
    (exposure: ExposureRange) =>
      sendEvent(excelerant, "exposure", exposure, "grow"),
    [excelerant]
  );

  const sendBloomExposure = useCallback(
    (exposure: ExposureRange) =>
      sendEvent(excelerant, "exposure", exposure, "bloom"),
    [excelerant]
  );

  const sendFanSpeed = useCallback(
    (fanSpeed: Number) => sendEvent(excelerant, "fanSpeed", fanSpeed),
    [excelerant]
  );

  return {
    growTemperature,
    bloomTemperature,
    growHumidity,
    bloomHumidity,
    growExposure,
    sendGrowExposure,
    bloomExposure,
    sendBloomExposure,
    growPower,
    sendGrowPower,
    bloomPower,
    sendBloomPower,
    fanSpeed,
    sendFanSpeed,
  };
}
