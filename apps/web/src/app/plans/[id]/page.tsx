"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, Mail, Calendar, Dumbbell, Clock, Heart } from "lucide-react";
import { createClient } from "@/lib/supabase/client";
import { formatDate, DAYS_OF_WEEK } from "@/lib/utils";
import type { WorkoutPlan, WorkoutDay } from "@/types";

export default function PlanDetailPage() {
  const params = useParams();
  const planId = params.id as string;

  const [plan, setPlan] = useState<WorkoutPlan | null>(null);
  const [days, setDays] = useState<WorkoutDay[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedWeek, setSelectedWeek] = useState(1);
  const [sendingEmail, setSendingEmail] = useState(false);

  useEffect(() => {
    fetchPlan();
  }, [planId]);

  const fetchPlan = async () => {
    try {
      const supabase = createClient();
      const { data: { session } } = await supabase.auth.getSession();

      if (!session) return;

      const response = await fetch(`/api/v1/plans/${planId}`, {
        headers: {
          Authorization: `Bearer ${session.access_token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setPlan(data.plan);
        setDays(data.days || []);
      }
    } catch (error) {
      console.error("Failed to fetch plan:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendEmail = async () => {
    setSendingEmail(true);
    try {
      const supabase = createClient();
      const { data: { session } } = await supabase.auth.getSession();

      if (!session) return;

      const response = await fetch(`/api/v1/plans/${planId}/send-email`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${session.access_token}`,
        },
      });

      if (response.ok) {
        alert("Plan sent successfully!");
      } else {
        alert("Failed to send email");
      }
    } catch {
      alert("Failed to send email");
    } finally {
      setSendingEmail(false);
    }
  };

  const weekDays = days.filter((day) => day.week_number === selectedWeek);

  if (loading) {
    return (
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
        <div className="h-4 bg-gray-200 rounded w-1/3 mb-8" />
        <div className="card">
          <div className="h-40 bg-gray-200 rounded" />
        </div>
      </div>
    );
  }

  if (!plan) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-semibold text-gray-900">Plan not found</h2>
        <Link href="/plans" className="btn-primary mt-4">
          Back to Plans
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <Link
          href="/plans"
          className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Plans
        </Link>

        <div className="mt-4 flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-gray-900">{plan.name}</h1>
              <span
                className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                  plan.status === "active"
                    ? "bg-green-100 text-green-700"
                    : plan.status === "completed"
                    ? "bg-gray-100 text-gray-700"
                    : "bg-yellow-100 text-yellow-700"
                }`}
              >
                {plan.status}
              </span>
            </div>
            <p className="mt-1 text-gray-600">
              {plan.weeks} weeks starting {formatDate(plan.start_date)}
            </p>
          </div>

          <button
            onClick={handleSendEmail}
            disabled={sendingEmail}
            className="btn-primary flex items-center gap-2"
          >
            <Mail className="h-4 w-4" />
            {sendingEmail ? "Sending..." : "Send to Client"}
          </button>
        </div>
      </div>

      {/* Week Selector */}
      <div className="mb-6">
        <div className="flex gap-2">
          {Array.from({ length: plan.weeks }, (_, i) => i + 1).map((week) => (
            <button
              key={week}
              onClick={() => setSelectedWeek(week)}
              className={`rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
                selectedWeek === week
                  ? "bg-primary-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              Week {week}
            </button>
          ))}
        </div>
      </div>

      {/* Week View */}
      <div className="grid gap-4 lg:grid-cols-7">
        {DAYS_OF_WEEK.map((dayName, dayIndex) => {
          const dayWorkout = weekDays.find((d) => d.day_of_week === dayIndex);

          return (
            <div
              key={dayName}
              className={`card ${
                dayWorkout ? "border-primary-200 bg-primary-50/50" : ""
              }`}
            >
              <h3 className="font-medium text-gray-900 mb-2">{dayName}</h3>

              {dayWorkout ? (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-sm text-primary-700">
                    <Dumbbell className="h-4 w-4" />
                    <span className="font-medium">{dayWorkout.focus}</span>
                  </div>

                  <div className="space-y-2">
                    {dayWorkout.exercises.map((exercise, idx) => (
                      <div
                        key={idx}
                        className="rounded-lg bg-white p-2 text-xs border"
                      >
                        <p className="font-medium text-gray-900">
                          {exercise.exercise_name}
                        </p>
                        {exercise.sets && exercise.reps && (
                          <p className="text-gray-600 flex items-center gap-1 mt-1">
                            <Dumbbell className="h-3 w-3" />
                            {exercise.sets} x {exercise.reps}
                            {exercise.weight_kg && ` @ ${exercise.weight_kg}kg`}
                          </p>
                        )}
                        {exercise.duration_minutes && (
                          <p className="text-gray-600 flex items-center gap-1 mt-1">
                            <Clock className="h-3 w-3" />
                            {exercise.duration_minutes} min
                            {exercise.distance_km && ` / ${exercise.distance_km}km`}
                          </p>
                        )}
                        {exercise.target_hr && (
                          <p className="text-gray-600 flex items-center gap-1 mt-1">
                            <Heart className="h-3 w-3" />
                            {exercise.target_hr} bpm
                          </p>
                        )}
                      </div>
                    ))}
                  </div>

                  {dayWorkout.notes && (
                    <p className="text-xs text-gray-500 italic">
                      {dayWorkout.notes}
                    </p>
                  )}
                </div>
              ) : (
                <p className="text-sm text-gray-500">Rest day</p>
              )}
            </div>
          );
        })}
      </div>

      {/* Coach Notes */}
      {plan.coach_notes && (
        <div className="mt-8 card">
          <h3 className="font-medium text-gray-900 mb-2">Coach Notes</h3>
          <p className="text-gray-600">{plan.coach_notes}</p>
        </div>
      )}
    </div>
  );
}
