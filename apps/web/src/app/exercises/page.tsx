"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import { Plus, Search, Filter, Play, Tag } from "lucide-react";
import { createClient } from "@/lib/supabase/client";
import { getYouTubeThumbnail, EXERCISE_CATEGORIES } from "@/lib/utils";
import type { Exercise, ExerciseCategory } from "@/types";

export default function ExercisesPage() {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [categoryFilter, setCategoryFilter] = useState<ExerciseCategory | "all">("all");

  useEffect(() => {
    fetchExercises();
  }, []);

  const fetchExercises = async () => {
    try {
      const supabase = createClient();
      const { data: { session } } = await supabase.auth.getSession();

      if (!session) return;

      const response = await fetch("/api/v1/exercises", {
        headers: {
          Authorization: `Bearer ${session.access_token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setExercises(data.exercises || []);
      }
    } catch (error) {
      console.error("Failed to fetch exercises:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredExercises = exercises.filter((exercise) => {
    const matchesSearch =
      exercise.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      exercise.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      exercise.manual_tags.some((tag) =>
        tag.toLowerCase().includes(searchQuery.toLowerCase())
      );
    const matchesCategory =
      categoryFilter === "all" || exercise.category === categoryFilter;
    return matchesSearch && matchesCategory;
  });

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Exercise Library</h1>
          <p className="mt-1 text-gray-600">
            Manage your exercise database with AI-enhanced tagging
          </p>
        </div>
        <Link href="/exercises/new" className="btn-primary flex items-center gap-2">
          <Plus className="h-4 w-4" />
          Add Exercise
        </Link>
      </div>

      {/* Filters */}
      <div className="card mb-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search exercises..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input pl-10"
            />
          </div>
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value as ExerciseCategory | "all")}
              className="input pl-10 pr-8 appearance-none"
            >
              <option value="all">All Categories</option>
              {EXERCISE_CATEGORIES.map((cat) => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Exercise Grid */}
      {loading ? (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="card animate-pulse">
              <div className="h-40 bg-gray-200 rounded-lg mb-4" />
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
              <div className="h-3 bg-gray-200 rounded w-1/2" />
            </div>
          ))}
        </div>
      ) : filteredExercises.length === 0 ? (
        <div className="card text-center py-12">
          <div className="mx-auto w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center mb-4">
            <Play className="h-6 w-6 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900">No exercises yet</h3>
          <p className="mt-1 text-gray-600">
            Get started by adding your first exercise
          </p>
          <Link href="/exercises/new" className="btn-primary mt-4 inline-flex items-center gap-2">
            <Plus className="h-4 w-4" />
            Add Exercise
          </Link>
        </div>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {filteredExercises.map((exercise) => (
            <Link
              key={exercise.id}
              href={`/exercises/${exercise.id}`}
              className="card hover:shadow-md transition-shadow"
            >
              {exercise.youtube_url && getYouTubeThumbnail(exercise.youtube_url) ? (
                <div className="relative h-40 -mx-6 -mt-6 mb-4 rounded-t-xl overflow-hidden">
                  <Image
                    src={getYouTubeThumbnail(exercise.youtube_url)!}
                    alt={exercise.name}
                    fill
                    className="object-cover"
                  />
                  <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
                    <div className="rounded-full bg-white/90 p-3">
                      <Play className="h-6 w-6 text-gray-900" />
                    </div>
                  </div>
                </div>
              ) : (
                <div className="h-40 -mx-6 -mt-6 mb-4 rounded-t-xl bg-gradient-to-br from-primary-100 to-accent-100 flex items-center justify-center">
                  <Play className="h-12 w-12 text-primary-400" />
                </div>
              )}

              <h3 className="font-semibold text-gray-900">{exercise.name}</h3>
              <p className="mt-1 text-sm text-gray-600 line-clamp-2">
                {exercise.description}
              </p>

              <div className="mt-3 flex flex-wrap gap-1">
                <span className="inline-flex items-center rounded-full bg-primary-100 px-2 py-0.5 text-xs font-medium text-primary-700">
                  {EXERCISE_CATEGORIES.find((c) => c.value === exercise.category)?.label}
                </span>
                {exercise.manual_tags.slice(0, 2).map((tag) => (
                  <span
                    key={tag}
                    className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600"
                  >
                    <Tag className="h-3 w-3" />
                    {tag}
                  </span>
                ))}
                {exercise.manual_tags.length > 2 && (
                  <span className="text-xs text-gray-500">
                    +{exercise.manual_tags.length - 2} more
                  </span>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
