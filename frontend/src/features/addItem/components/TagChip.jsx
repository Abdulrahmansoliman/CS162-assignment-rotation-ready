export default function TagChip({ tag, value, onValueChange, onRemove }) {
  return (
    <div className="flex flex-col gap-2 bg-gray-800 p-3 rounded-lg">
      <div className="flex justify-between items-center">
        <span className="text-white">{tag.name}</span>
        <button onClick={() => onRemove(tag.tag_id)} className="text-red-400">
          ✕
        </button>
      </div>

      <input
        className="bg-gray-700 text-white px-3 py-2 rounded-md"
        placeholder={`Enter ${tag.value_type} value`}
        value={value}
        onChange={(e) => onValueChange(tag.tag_id, e.target.value)}
      />
    </div>
  );
}



