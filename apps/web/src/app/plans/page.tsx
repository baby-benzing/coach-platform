"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Calendar, Search, Mail, Eye } from "lucide-react";
import { createClient } from "@/lib/supabase/client";
import { formatDate } from "@/lib/utils";
import type { WorkoutPlan } from "@/types";

export default function PlansPage() {
  const [plans, setPlans] = useState<WorkoutPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    fetchPlans();
  }, []);

  const fetchPlans = async () => {
    try {
      const supabase = createClient();
      const { data: { session } } = await supabase.auth.getSession();

      if (!session) return;

      const response = await fetch("/api/v1/plans", {
        headers: {
          Authorization: `Bearer ${session.access_token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setPlans(data.plans || []);
      }
    } catch (error) {
      console.error("Failed to fetch plans:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredPlans = plans.filter((plan) =>
    plan.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const getStatusColor = (status: WorkoutPlan["status"]) => {
    switch (status) {
      case "active":
        return "bg-green-100 text-green-700";
      case "completed":
        return "bg-gray-100 text-gray-700";
      case "draft":
        return "bg-yellow-100 text-yellow-700";
      default:
        return "bg-gray-100 text-gray-700";
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Workout Plans</h1>
          <p className="mt-1 text-gray-600">
            View and manage generated workout plans
          </p>
        </div>
      </div>

      {/* Search */}
      <div className="card mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search plans..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input pl-10"
          />
        </div>
      </div>

      {/* Plans List */}
      {loading ? (
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="card animate-pulse">
              <div className="h-6 bg-gray-200 rounded w-1/3 mb-3" />
              <div className="h-4 bg-gray-200 rounded w-1/2" />
            </div>
          ))}
        </div>
      ) : filteredPlans.length === 0 ? (
        <div className="card text-center py-12">
          <div className="mx-auto w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center mb-4">
            <Calendar className="h-6 w-6 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900">
            No workout plans yet
          </h3>
          <p className="mt-1 text-gray-600">
            Create a client assessment to generate workout plans
          </p>
          <Link href="/clients" className="btn-primary mt-4 inline-block">
            Go to Clients
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredPlans.map((plan) => (
            <div
              key={plan.id}
              className="card flex items-center justify-between"
            >
              <div>
                <div className="flex items-center gap-3">
                  <h3 className="font-semibold text-gray-900">{plan.name}</h3>
                  <span
                    className={`rounded-full px-2 py-0.5 text-xs font-medium ${getStatusColor(
                      plan.status
                    )}`}
                  >
                    {plan.status}
                  </span>
                </div>
                <p className="mt-1 text-sm text-gray-600">
                  {plan.weeks} weeks &bull; Starting {formatDate(plan.start_date)}
                </p>
                {plan.coach_notes && (
                  <p className="mt-2 text-sm text-gray-500 line-clamp-1">
                    {plan.coach_notes}
                  </p>
                )}
              </div>

              <div className="flex items-center gap-2">
                <Link
                  href={`/plans/${plan.id}`}
                  className="btn-secondary flex items-center gap-1 text-sm"
                >
                  <Eye className="h-4 w-4" />
                  View
                </Link>
                <button
                  onClick={async () => {
                    const supabase = createClient();
                    const { data: { session } } = await supabase.auth.getSession();
                    if (!session) return;

                    await fetch(`/api/v1/plans/${plan.id}/send-email`, {
                      method: "POST",
                      headers: {
                        Authorization: `Bearer ${session.access_token}`,
                      },
                    });
                    alert("Plan sent via email!");
                  }}
                  className="btn-primary flex items-center gap-1 text-sm"
                >
                  <Mail className="h-4 w-4" />
                  Send
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
