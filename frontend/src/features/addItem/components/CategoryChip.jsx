export default function CategoryChip({ category, onRemove, localeColor }) {
  return (
    <div className="px-3 py-1 text-white rounded-full flex items-center gap-2" style={{ backgroundColor: localeColor || '#374151' }}>
      <span>{category.category_name}</span>
      <button onClick={() => onRemove(category.category_id)} className="text-red-300 hover:text-red-100 transition-colors">
        ✕
      </button>
    </div>
  );
}

