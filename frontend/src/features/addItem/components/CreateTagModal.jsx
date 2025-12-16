import { useState, useRef, useEffect } from "react";

export default function CreateTagModal({ isOpen, onClose, onCreate }) {
  const [name, setName] = useState("");
  const [valueType, setValueType] = useState("");
  const [value, setValue] = useState("");
  
  const modalRef = useRef(null);

  if (!isOpen) return null;

  const handleOverlayClick = (e) => {
    if (modalRef.current && !modalRef.current.contains(e.target)) {
      onClose();
    }
  };

  function handleSubmit() {
    if (!name || !valueType || value === "") return;

    onCreate({
      name,
      value_type: valueType,
      value:
        valueType === "boolean"
          ? value === "true"
          : valueType === "numeric"
          ? Number(value)
          : value,
    });

    setName("");
    setValueType("");
    setValue("");
    onClose();
  }

  return (
    <div 
      className="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
      onClick={handleOverlayClick}
    >
      <div className="bg-gray-900 p-6 rounded-xl w-[400px] shadow-xl" ref={modalRef}>
        <h2 className="text-xl font-semibold text-white mb-4">
          Create New Tag
        </h2>

        {/* Tag Name */}
        <label className="text-gray-300">Tag Name</label>
        <input
          className="bg-gray-700 text-white px-3 py-2 rounded-md w-full mb-4"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        {/* Value Type */}
        <label className="text-gray-300">Value Type</label>
        <select
          className="bg-gray-700 text-white px-3 py-2 rounded-md w-full mb-4"
          value={valueType}
          onChange={(e) => {
            setValueType(e.target.value);
            setValue(""); // reset value when type changes
          }}
        >
          <option value="">Select type</option>
          <option value="text">Text</option>
          <option value="boolean">Boolean</option>
          <option value="numeric">Numeric</option>
        </select>

        {/* Value Input — dynamic */}
        <label className="text-gray-300">Value</label>

        {valueType === "numeric" && (
          <input
            type="number"
            className="bg-gray-700 text-white px-3 py-2 rounded-md w-full mb-6"
            value={value}
            onChange={(e) => setValue(e.target.value)}
          />
        )}

        {valueType === "boolean" && (
          <select
            className="bg-gray-700 text-white px-3 py-2 rounded-md w-full mb-6"
            value={value}
            onChange={(e) => setValue(e.target.value)}
          >
            <option value="">Select yes/no</option>
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        )}

        {valueType === "text" && (
          <input
            type="text"
            className="bg-gray-700 text-white px-3 py-2 rounded-md w-full mb-6"
            value={value}
            onChange={(e) => setValue(e.target.value)}
          />
        )}

        {/* Buttons */}
        <div className="flex justify-end gap-3">
          <button className="text-gray-300" onClick={onClose}>
            Cancel
          </button>
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded-md"
            onClick={handleSubmit}
          >
            Create Tag
          </button>
        </div>
      </div>
    </div>
  );
}


