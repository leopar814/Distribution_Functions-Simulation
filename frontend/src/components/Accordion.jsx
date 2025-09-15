import { useState } from "react";

export default function Accordion({ title, children }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="w-full rounded-md shadow-sm">
      {/* Botón */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex justify-between items-center p-4 bg-gray-100 hover:bg-gray-200 transition-colors duration-200"
      >
        <span className="font-semibold text-gray-800">{title}</span>
        <span className="text-xl">
          {isOpen ? "˄" : "–"}
        </span>
      </button>

      {/* Contenido desplegable */}
      <div
        className={`overflow-hidden transition-[max-height] duration-400 ease-in-out ${
          isOpen ? "max-h-screen" : "max-h-0"
        }`}
      >
        <div className="p-4 bg-white text-gray-700 break-words">
          {children}
        </div>
      </div>
    </div>
  );
}
