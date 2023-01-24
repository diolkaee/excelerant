import { ReactComponent as Power } from "../assets/power.svg";
import { ExposureRange } from "../hooks/useExcelerant";

interface ChamberProps {
  hasPower: boolean;
  setHasPower: (hasPower: boolean) => void;
  currentTemperature: number;
  currentHumidity: number;
  exposure: ExposureRange;
  setExposure: (exposure: ExposureRange) => void;
  className?: string;
}

export default function Chamber({
  hasPower,
  setHasPower,
  currentTemperature,
  currentHumidity,
  exposure,
  setExposure,
  className,
}: ChamberProps) {
  return (
    <div
      className={`flex flex-col px-2 lg:px-16 justify-between items-center text-2xl lg:text-4xl 2xl:text-9xl text-crystalwhite ${className}`}
    >
      <p>{currentTemperature} C°</p>
      <hr className="border-excelerant border border-t-2 w-full" />
      <p>{currentHumidity} %</p>
      <hr className="border-excelerant border border-t-2 w-full" />
      <button className="border-4 shadow-crystalwhite border-white bg-crystalwhite rounded-xl text-black p-4">
        {createClock(exposure.duration.hour, exposure.duration.minute)}
      </button>
      <hr className="border-excelerant border border-t-2 w-full" />
      <Power
        className={`${
          hasPower ? "fill-green-300" : "fill-red-300"
        } h-20 lg:h-40`}
        onClick={() => setHasPower(!hasPower)}
      />
    </div>
  );
}

function createClock(hour: number, minute: number) {
  var formattedHour = ("0" + hour).slice(-2);
  var formattedMinute = ("0" + minute).slice(-2);
  return minute
    ? `${formattedHour}:${formattedMinute} h`
    : `${formattedHour} h`;
}
