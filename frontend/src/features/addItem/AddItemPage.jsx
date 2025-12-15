import { useEffect, useState } from "react";
import SearchSelect from "./components/SearchSelect";

import { getCategories } from "@/api/category";
import { getTags } from "@/api/tag";
import { createItem } from "@/api/item";

import CategoryChip from "./components/CategoryChip";
import TagChip from "./components/TagChip";
import CreateTagModal from "./components/CreateTagModal";

export default function AddItemPage() {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [walkingDistance, setWalkingDistance] = useState("");

  const [categories, setCategories] = useState([]);
  const [selectedCategories, setSelectedCategories] = useState([]);

  const [tags, setTags] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);
  const [existingTagValues, setExistingTagValues] = useState({});

  const [newTags, setNewTags] = useState([]);

  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    async function load() {
      const cat = await getCategories();
      const tg = await getTags();
      setCategories(cat);
      setTags(tg);
    }
    load();
  }, []);

  function addCategory(id) {
    const cat = categories.find((c) => c.category_id === id);
    if (!cat) return;
    setSelectedCategories((prev) => [...prev, cat]);
  }

  function removeCategory(id) {
    setSelectedCategories((prev) => prev.filter((c) => c.category_id !== id));
  }

  function addTag(id) {
    const tag = tags.find((t) => t.tag_id === id);
    if (!tag) return;
    setSelectedTags((prev) => [...prev, tag]);
  }

  function removeTag(id) {
    setExistingTagValues((prev) => {
      const copy = { ...prev };
      delete copy[id];
      return copy;
    });

    setSelectedTags((prev) => prev.filter((t) => t.tag_id !== id));
  }

  function handleExistingTagValueChange(id, value) {
    setExistingTagValues((prev) => ({ ...prev, [id]: value }));
  }

  function handleCreateNewTag(tagObj) {
    setNewTags((prev) => [...prev, tagObj]);
  }

  async function handleSubmit() {
    const body = {
      name,
      location,
      walking_distance: parseFloat(walkingDistance),

      category_ids: selectedCategories.map((c) => c.category_id),

      existing_tags: selectedTags.map((tag) => ({
        tag_id: tag.tag_id,
        value: existingTagValues[tag.tag_id] || "",
      })),

      new_tags: newTags.map((tag) => ({
        name: tag.name,
        value_type: tag.value_type,
        value: tag.value,
      })),
    };

    await createItem(body);
    alert("Item created!");
  }

  return (
    <div className="flex justify-center p-10">
      <div className="bg-gray-900 p-10 rounded-xl shadow-xl w-[650px]">
        <h1 className="text-3xl font-bold text-white mb-8">Add Item</h1>

        {/* NAME */}
        <label className="text-gray-300">Name</label>
        <input
          className="bg-gray-700 text-white px-3 py-2 rounded-md w-full mb-6"
          placeholder="Enter item name (e.g., Gym, Café, Pharmacy)"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        {/* LOCATION */}
        <label className="text-gray-300">Location</label>
        <input
          className="bg-gray-700 text-white px-3 py-2 rounded-md w-full mb-6"
          placeholder="Enter location or address"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />

        {/* WALKING DISTANCE */}
        <label className="text-gray-300">Walking Distance (meters)</label>
        <input
          className="bg-gray-700 text-white px-3 py-2 rounded-md w-full mb-6"
          placeholder="Distance in meters (e.g., 300)"
          value={walkingDistance}
          onChange={(e) => setWalkingDistance(e.target.value)}
        />

        {/* CATEGORIES */}
        <label className="text-gray-300">Categories</label>
        <SearchSelect
          placeholder="Search categories..."
          items={categories.map((c) => ({
            id: c.category_id,
            label: c.category_name,
          }))}
          onSelect={(id) => addCategory(parseInt(id))}
          selectedItems={selectedCategories.map((c) => c.category_id)}
        />

        <div className="flex flex-wrap gap-2 mb-6">
          {selectedCategories.map((cat) => (
            <CategoryChip
              key={cat.category_id}
              category={cat}
              onRemove={removeCategory}
            />
          ))}
        </div>

        {/* TAGS */}
        <label className="text-gray-300">Tags</label>
        <SearchSelect
          placeholder="Search tags..."
          items={tags.map((t) => ({
            id: t.tag_id,
            label: t.name,
          }))}
          onSelect={(id) => addTag(parseInt(id))}
          selectedItems={selectedTags.map((t) => t.tag_id)}
        />

        {/* EXISTING + NEW TAGS */}
        <div className="flex flex-col gap-3 mb-6">
          {selectedTags.map((tag) => (
            <TagChip
              key={tag.tag_id}
              tag={tag}
              value={existingTagValues[tag.tag_id] || ""}
              onValueChange={handleExistingTagValueChange}
              onRemove={removeTag}
            />
          ))}

          {newTags.map((tag, index) => (
            <TagChip
              key={`new-${index}`}
              tag={tag}
              value={tag.value}
              onValueChange={(ignoredId, value) => {
                const updated = [...newTags];
                updated[index].value = value;
                setNewTags(updated);
              }}
              onRemove={() => {
                setNewTags((prev) => prev.filter((_, i) => i !== index));
              }}
            />
          ))}
        </div>

        {/* CREATE TAG */}
        <button
          className="text-blue-400 mb-6"
          onClick={() => setModalOpen(true)}
        >
          + Create new tag
        </button>

        {/* SUBMIT */}
        <button
          className="bg-blue-600 hover:bg-blue-700 text-white w-full py-3 rounded-md"
          onClick={handleSubmit}
        >
          Create Item
        </button>

        {/* MODAL */}
        <CreateTagModal
          isOpen={modalOpen}
          onClose={() => setModalOpen(false)}
          onCreate={handleCreateNewTag}
        />
      </div>
    </div>
  );
}








