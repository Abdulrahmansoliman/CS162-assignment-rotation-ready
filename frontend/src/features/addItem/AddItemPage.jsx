import { useEffect, useState } from "react";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/shared/components/ui/select";
import { Spinner } from "@/shared/components/ui/spinner";

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
    setSelectedTagValues((prev) => {
      const copy = { ...prev };
      delete copy[id];
      return copy;
    });

    setSelectedTags((prev) => prev.filter((t) => t.tag_id !== id));
  }

  function setSelectedTagValues(updater) {
    setExistingTagValues((prev) => {
      const updated = typeof updater === "function" ? updater(prev) : updater;
      return updated;
    });
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

        <label className="text-gray-300">Name</label>
        <input
          className="bg-gray-700 text-white px-3 py-2 rounded-md w-full mb-6"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <label className="text-gray-300">Location</label>
        <input
          className="bg-gray-700 text-white px-3 py-2 rounded-md w-full mb-6"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />

        <label className="text-gray-300">Walking Distance (meters)</label>
        <input
          className="bg-gray-700 text-white px-3 py-2 rounded-md w-full mb-6"
          value={walkingDistance}
          onChange={(e) => setWalkingDistance(e.target.value)}
        />

        {/* Categories */}
        <label className="text-gray-300">Categories</label>

        <Select onValueChange={(v) => addCategory(parseInt(v))}>
          <SelectTrigger className="bg-gray-700 text-white w-full mb-3">
            <SelectValue placeholder="Select a category" />
          </SelectTrigger>
          <SelectContent>
            {categories
              .filter((c) => !selectedCategories.some((s) => s.category_id === c.category_id))
              .map((c) => (
                <SelectItem key={c.category_id} value={String(c.category_id)}>
                  {c.category_name}
                </SelectItem>
              ))}
          </SelectContent>
        </Select>

        <div className="flex flex-wrap gap-2 mb-6">
          {selectedCategories.map((cat) => (
            <CategoryChip key={cat.category_id} category={cat} onRemove={removeCategory} />
          ))}
        </div>

        {/* Tags */}
        <label className="text-gray-300">Tags</label>

        <Select onValueChange={(v) => addTag(parseInt(v))}>
          <SelectTrigger className="bg-gray-700 text-white w-full mb-3">
            <SelectValue placeholder="Select a tag" />
          </SelectTrigger>
          <SelectContent>
            {tags
              .filter((t) => !selectedTags.some((s) => s.tag_id === t.tag_id))
              .map((t) => (
                <SelectItem key={t.tag_id} value={String(t.tag_id)}>
                  {t.name}
                </SelectItem>
              ))}
          </SelectContent>
        </Select>

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
        </div>

        <button
          className="text-blue-400 mb-6"
          onClick={() => setModalOpen(true)}
        >
          + Create new tag
        </button>

        <button
          className="bg-blue-600 hover:bg-blue-700 text-white w-full py-3 rounded-md"
          onClick={handleSubmit}
        >
          Create Item
        </button>

        <CreateTagModal
          isOpen={modalOpen}
          onClose={() => setModalOpen(false)}
          onCreate={handleCreateNewTag}
        />
      </div>
    </div>
  );
}




