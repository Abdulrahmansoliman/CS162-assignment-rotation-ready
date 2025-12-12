export default function TagChip({ tag, value, onValueChange, onRemove }) {
  function handleChange(e) {
    let val = e.target.value;

    if (tag.value_type === "boolean") {
      val = val === "true";
    }

    if (tag.value_type === "numeric") {
      val = Number(val);
    }

    onValueChange(tag.tag_id, val);
  }

  return (
    <div className="flex flex-col gap-2 bg-gray-800 p-3 rounded-lg">
      <div className="flex justify-between items-center">
        <span className="text-white">{tag.name}</span>
        <button 
          onClick={() => onRemove(tag.tag_id)} 
          className="text-red-400"
        >
          ✕
        </button>
      </div>

      {/* NUMERIC */}
      {tag.value_type === "numeric" && (
        <input
          type="number"
          className="bg-gray-700 text-white px-3 py-2 rounded-md"
          placeholder="Enter numeric value"
          value={value}
          onChange={handleChange}
        />
      )}

      {/* BOOLEAN */}
      {tag.value_type === "boolean" && (
        <select
          className="bg-gray-700 text-white px-3 py-2 rounded-md"
          value={value === true ? "true" : value === false ? "false" : ""}
          onChange={handleChange}
        >
          <option value="">Select yes/no</option>
          <option value="true">Yes</option>
          <option value="false">No</option>
        </select>
      )}

      {/* TEXT */}
      {tag.value_type === "text" && (
        <input
          type="text"
          className="bg-gray-700 text-white px-3 py-2 rounded-md"
          placeholder="Enter text value"
          value={value}
          onChange={handleChange}
        />
      )}
    </div>
  );
}





