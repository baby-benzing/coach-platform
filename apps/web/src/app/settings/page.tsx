"use client";

import { useState, useEffect } from "react";
import { Loader2, Save } from "lucide-react";
import { createClient } from "@/lib/supabase/client";

export default function SettingsPage() {
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);

  const [profile, setProfile] = useState({
    name: "",
    email: "",
    training_philosophy: "",
    specializations: [] as string[],
  });

  const [specializationInput, setSpecializationInput] = useState("");

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    const supabase = createClient();
    const { data: { user } } = await supabase.auth.getUser();

    if (user) {
      setProfile({
        name: user.user_metadata?.name || "",
        email: user.email || "",
        training_philosophy: user.user_metadata?.training_philosophy || "",
        specializations: user.user_metadata?.specializations || [],
      });
    }
  };

  const handleSave = async () => {
    setLoading(true);
    setSaved(false);

    try {
      const supabase = createClient();
      await supabase.auth.updateUser({
        data: {
          name: profile.name,
          training_philosophy: profile.training_philosophy,
          specializations: profile.specializations,
        },
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (error) {
      console.error("Failed to save:", error);
    } finally {
      setLoading(false);
    }
  };

  const addSpecialization = () => {
    if (
      specializationInput.trim() &&
      !profile.specializations.includes(specializationInput.trim())
    ) {
      setProfile({
        ...profile,
        specializations: [...profile.specializations, specializationInput.trim()],
      });
      setSpecializationInput("");
    }
  };

  const removeSpecialization = (spec: string) => {
    setProfile({
      ...profile,
      specializations: profile.specializations.filter((s) => s !== spec),
    });
  };

  return (
    <div className="max-w-2xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="mt-1 text-gray-600">
          Manage your profile and training philosophy
        </p>
      </div>

      <div className="space-y-6">
        {/* Profile Section */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Profile</h2>

          <div className="space-y-4">
            <div>
              <label className="label">Name</label>
              <input
                type="text"
                value={profile.name}
                onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                className="input mt-1"
              />
            </div>

            <div>
              <label className="label">Email</label>
              <input
                type="email"
                value={profile.email}
                disabled
                className="input mt-1 bg-gray-50"
              />
              <p className="mt-1 text-xs text-gray-500">
                Email cannot be changed
              </p>
            </div>
          </div>
        </div>

        {/* Training Philosophy */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Training Philosophy
          </h2>
          <p className="text-sm text-gray-600 mb-4">
            This will be used to guide the AI when generating workout plans for
            your clients.
          </p>

          <textarea
            value={profile.training_philosophy}
            onChange={(e) =>
              setProfile({ ...profile, training_philosophy: e.target.value })
            }
            className="input min-h-[150px]"
            placeholder="Describe your training philosophy, preferred methodologies, and key principles you follow when designing programs..."
          />
        </div>

        {/* Specializations */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Specializations
          </h2>

          <div className="flex gap-2 mb-4">
            <input
              type="text"
              value={specializationInput}
              onChange={(e) => setSpecializationInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  addSpecialization();
                }
              }}
              className="input flex-1"
              placeholder="e.g., Powerlifting, HIIT, Mobility"
            />
            <button
              type="button"
              onClick={addSpecialization}
              className="btn-secondary"
            >
              Add
            </button>
          </div>

          {profile.specializations.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {profile.specializations.map((spec) => (
                <span
                  key={spec}
                  className="inline-flex items-center gap-1 rounded-full bg-primary-100 px-3 py-1 text-sm text-primary-700"
                >
                  {spec}
                  <button
                    type="button"
                    onClick={() => removeSpecialization(spec)}
                    className="hover:text-primary-900"
                  >
                    &times;
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Save Button */}
        <div className="flex items-center gap-4">
          <button
            onClick={handleSave}
            disabled={loading}
            className="btn-primary flex items-center gap-2"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Save className="h-4 w-4" />
            )}
            Save Changes
          </button>
          {saved && (
            <span className="text-sm text-green-600">Changes saved!</span>
          )}
        </div>
      </div>
    </div>
  );
}
