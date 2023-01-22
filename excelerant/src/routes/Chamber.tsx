import { ReactComponent as Power } from "../assets/power.svg";

interface ChamberProps {
  hasPower: boolean;
  setHasPower: (hasPower: boolean) => void;
  currentTemperature: number;
  targetTemperature: number;
  setTargetTemperature: (temperatureC: number) => void;
  currentHumidity: number;
  targetHumidity: number;
  setTargetHumidity: (humidity: number) => void;
  className?: string;
}

export default function Chamber({
  hasPower,
  setHasPower,
  currentTemperature,
  targetTemperature,
  setTargetTemperature,
  currentHumidity,
  targetHumidity,
  setTargetHumidity,
  className,
}: ChamberProps) {
  return (
    <div
      className={`flex flex-col px-16 justify-between items-center text-4xl ${className}`}
    >
      <div className="flex flex-col w-full">
        <div className="flex items-center justify-center">
          <p>{currentTemperature} C°</p>
          {currentTemperature !== targetTemperature && (
            <p className="ml-3 text-gray-400">({targetTemperature}C°)</p>
          )}
        </div>
        <input
          type="range"
          min={20}
          max={50}
          value={targetTemperature}
          onChange={(ev) => setTargetTemperature(parseInt(ev.target.value))}
          className="mt-4"
        />
      </div>
      <div className="flex flex-col w-full">
        <div className="flex items-center justify-center">
          <p>{currentHumidity} %</p>
          {currentHumidity !== targetHumidity && (
            <p className="ml-3 text-gray-400">({targetHumidity}%)</p>
          )}
        </div>
        <input
          type="range"
          min={0}
          max={100}
          value={targetHumidity}
          onChange={(ev) => setTargetHumidity(parseInt(ev.target.value))}
          className="mt-4"
        />
      </div>
      <Power
        className={`${hasPower ? "fill-green-300" : "fill-red-300"} w-1/2`}
        onClick={() => setHasPower(!hasPower)}
      >
        {hasPower ? "Ausschalten" : "Anschalten"}
      </Power>
    </div>
  );
}
