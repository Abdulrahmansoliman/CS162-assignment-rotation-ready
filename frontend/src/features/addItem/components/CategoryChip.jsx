export default function CategoryChip({ category, onRemove }) {
  return (
    <div className="px-3 py-1 bg-gray-700 text-white rounded-full flex items-center gap-2">
      <span>{category.name}</span>
      <button onClick={() => onRemove(category.category_id)} className="text-red-400">
        ✕
      </button>
    </div>
  );
}

