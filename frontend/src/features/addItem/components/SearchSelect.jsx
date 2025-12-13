import { useState } from "react";

export default function SearchSelect({ items, displayField, valueField, onSelect, placeholder }) {
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);

  const filtered = items.filter((item) =>
    item[displayField].toLowerCase().includes(query.toLowerCase())
  );

  function handleSelect(item) {
    onSelect(item[valueField]);
    setQuery("");
    setOpen(false);
  }

  return (
    <div className="relative w-full">
      <input
        className="w-full bg-gray-700 text-white px-3 py-2 rounded-md"
        placeholder={placeholder}
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setOpen(true);
        }}
        onFocus={() => setOpen(true)}
      />

      {open && (
        <div className="absolute mt-1 w-full bg-gray-800 text-white rounded-md shadow-lg max-h-48 overflow-auto z-20">
          {filtered.length === 0 && (
            <div className="p-2 text-gray-400">No results</div>
          )}

          {filtered.map((item) => (
            <div
              key={item[valueField]}
              className="px-3 py-2 hover:bg-gray-700 cursor-pointer"
              onClick={() => handleSelect(item)}
            >
              {item[displayField]}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

