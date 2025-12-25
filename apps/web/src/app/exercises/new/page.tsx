"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Loader2, Plus, X, Sparkles } from "lucide-react";
import { createClient } from "@/lib/supabase/client";
import { EXERCISE_CATEGORIES, EQUIPMENT_OPTIONS } from "@/lib/utils";
import type { ExerciseCategory } from "@/types";

export default function NewExercisePage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [aiTagsLoading, setAiTagsLoading] = useState(false);

  const [formData, setFormData] = useState({
    name: "",
    description: "",
    youtube_url: "",
    category: "strength" as ExerciseCategory,
    manual_tags: [] as string[],
    equipment: [] as string[],
  });
  const [tagInput, setTagInput] = useState("");

  const addTag = () => {
    if (tagInput.trim() && !formData.manual_tags.includes(tagInput.trim())) {
      setFormData({
        ...formData,
        manual_tags: [...formData.manual_tags, tagInput.trim()],
      });
      setTagInput("");
    }
  };

  const removeTag = (tag: string) => {
    setFormData({
      ...formData,
      manual_tags: formData.manual_tags.filter((t) => t !== tag),
    });
  };

  const toggleEquipment = (equipment: string) => {
    setFormData({
      ...formData,
      equipment: formData.equipment.includes(equipment)
        ? formData.equipment.filter((e) => e !== equipment)
        : [...formData.equipment, equipment],
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const supabase = createClient();
      const { data: { session } } = await supabase.auth.getSession();

      if (!session) {
        throw new Error("Not authenticated");
      }

      const response = await fetch("/api/v1/exercises", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session.access_token}`,
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Failed to create exercise");
      }

      router.push("/exercises");
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl">
      <div className="mb-8">
        <Link
          href="/exercises"
          className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Exercises
        </Link>
        <h1 className="mt-4 text-2xl font-bold text-gray-900">Add New Exercise</h1>
        <p className="mt-1 text-gray-600">
          Add an exercise to your library. AI will automatically suggest additional tags.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {error && (
          <div className="rounded-lg bg-red-50 p-4 text-sm text-red-600">
            {error}
          </div>
        )}

        <div className="card space-y-6">
          {/* Name */}
          <div>
            <label htmlFor="name" className="label">
              Exercise Name *
            </label>
            <input
              id="name"
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="input mt-1"
              placeholder="e.g., Barbell Back Squat"
              required
            />
          </div>

          {/* Description */}
          <div>
            <label htmlFor="description" className="label">
              Description *
            </label>
            <textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="input mt-1 min-h-[100px]"
              placeholder="Describe the exercise, key form cues, and benefits..."
              required
            />
          </div>

          {/* YouTube URL */}
          <div>
            <label htmlFor="youtube_url" className="label">
              YouTube Video URL
            </label>
            <input
              id="youtube_url"
              type="url"
              value={formData.youtube_url}
              onChange={(e) => setFormData({ ...formData, youtube_url: e.target.value })}
              className="input mt-1"
              placeholder="https://youtube.com/watch?v=..."
            />
            <p className="mt-1 text-xs text-gray-500">
              Add a video demonstration for your clients
            </p>
          </div>

          {/* Category */}
          <div>
            <label htmlFor="category" className="label">
              Category *
            </label>
            <select
              id="category"
              value={formData.category}
              onChange={(e) =>
                setFormData({ ...formData, category: e.target.value as ExerciseCategory })
              }
              className="input mt-1"
              required
            >
              {EXERCISE_CATEGORIES.map((cat) => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>
          </div>

          {/* Manual Tags */}
          <div>
            <label className="label">Tags</label>
            <div className="mt-1 flex gap-2">
              <input
                type="text"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    addTag();
                  }
                }}
                className="input flex-1"
                placeholder="Add a tag and press Enter"
              />
              <button
                type="button"
                onClick={addTag}
                className="btn-secondary"
              >
                <Plus className="h-4 w-4" />
              </button>
            </div>
            {formData.manual_tags.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {formData.manual_tags.map((tag) => (
                  <span
                    key={tag}
                    className="inline-flex items-center gap-1 rounded-full bg-primary-100 px-3 py-1 text-sm text-primary-700"
                  >
                    {tag}
                    <button
                      type="button"
                      onClick={() => removeTag(tag)}
                      className="hover:text-primary-900"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </span>
                ))}
              </div>
            )}
            <div className="mt-2 flex items-center gap-2 text-xs text-gray-500">
              <Sparkles className="h-3 w-3" />
              AI will automatically suggest additional tags based on your description
            </div>
          </div>

          {/* Equipment */}
          <div>
            <label className="label">Equipment Required</label>
            <div className="mt-2 flex flex-wrap gap-2">
              {EQUIPMENT_OPTIONS.map((equipment) => (
                <button
                  key={equipment}
                  type="button"
                  onClick={() => toggleEquipment(equipment)}
                  className={`rounded-full px-3 py-1 text-sm transition-colors ${
                    formData.equipment.includes(equipment)
                      ? "bg-primary-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  {equipment}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Submit */}
        <div className="flex items-center gap-4">
          <button
            type="submit"
            disabled={loading}
            className="btn-primary"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Saving...
              </>
            ) : (
              "Save Exercise"
            )}
          </button>
          <Link href="/exercises" className="btn-secondary">
            Cancel
          </Link>
        </div>
      </form>
    </div>
  );
}
