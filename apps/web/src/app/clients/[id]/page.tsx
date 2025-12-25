"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  ArrowLeft,
  ClipboardList,
  Calendar,
  TrendingUp,
  Plus,
  Sparkles,
} from "lucide-react";
import { createClient } from "@/lib/supabase/client";
import { formatDate } from "@/lib/utils";
import type { Client, Assessment, WorkoutPlan } from "@/types";

export default function ClientDetailPage() {
  const params = useParams();
  const clientId = params.id as string;

  const [client, setClient] = useState<Client | null>(null);
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [plans, setPlans] = useState<WorkoutPlan[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchClientData();
  }, [clientId]);

  const fetchClientData = async () => {
    try {
      const supabase = createClient();
      const { data: { session } } = await supabase.auth.getSession();

      if (!session) return;

      const headers = {
        Authorization: `Bearer ${session.access_token}`,
      };

      // Fetch client details
      const clientRes = await fetch(`/api/v1/clients/${clientId}`, { headers });
      if (clientRes.ok) {
        const clientData = await clientRes.json();
        setClient(clientData);
      }

      // Fetch assessments
      const assessmentsRes = await fetch(
        `/api/v1/clients/${clientId}/assessments`,
        { headers }
      );
      if (assessmentsRes.ok) {
        const assessmentsData = await assessmentsRes.json();
        setAssessments(assessmentsData.assessments || []);
      }

      // Fetch plans
      const plansRes = await fetch(`/api/v1/plans?client_id=${clientId}`, {
        headers,
      });
      if (plansRes.ok) {
        const plansData = await plansRes.json();
        setPlans(plansData.plans || []);
      }
    } catch (error) {
      console.error("Failed to fetch client data:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
        <div className="h-4 bg-gray-200 rounded w-1/3 mb-8" />
        <div className="card">
          <div className="h-20 bg-gray-200 rounded" />
        </div>
      </div>
    );
  }

  if (!client) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-semibold text-gray-900">Client not found</h2>
        <Link href="/clients" className="btn-primary mt-4">
          Back to Clients
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <Link
          href="/clients"
          className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Clients
        </Link>

        <div className="mt-4 flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className="h-16 w-16 rounded-full bg-gradient-to-br from-primary-400 to-accent-400 flex items-center justify-center text-white font-bold text-2xl">
              {client.name.charAt(0).toUpperCase()}
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{client.name}</h1>
              <p className="text-gray-600">{client.email}</p>
            </div>
          </div>

          <Link
            href={`/clients/${clientId}/assessment`}
            className="btn-primary flex items-center gap-2"
          >
            <ClipboardList className="h-4 w-4" />
            New Assessment
          </Link>
        </div>
      </div>

      {/* Stats */}
      <div className="grid gap-4 sm:grid-cols-3 mb-8">
        <div className="card">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-primary-100 p-2">
              <TrendingUp className="h-5 w-5 text-primary-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Assessments</p>
              <p className="text-2xl font-bold text-gray-900">
                {assessments.length}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-green-100 p-2">
              <Calendar className="h-5 w-5 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Workout Plans</p>
              <p className="text-2xl font-bold text-gray-900">{plans.length}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-accent-100 p-2">
              <Calendar className="h-5 w-5 text-accent-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Client Since</p>
              <p className="text-lg font-semibold text-gray-900">
                {formatDate(client.created_at)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Assessments */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Assessments</h2>
          <Link
            href={`/clients/${clientId}/assessment`}
            className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1"
          >
            <Plus className="h-4 w-4" />
            New Assessment
          </Link>
        </div>

        {assessments.length === 0 ? (
          <div className="card text-center py-8">
            <ClipboardList className="h-8 w-8 text-gray-400 mx-auto mb-2" />
            <p className="text-gray-600">No assessments yet</p>
            <Link
              href={`/clients/${clientId}/assessment`}
              className="btn-primary mt-4 inline-flex items-center gap-2"
            >
              <Plus className="h-4 w-4" />
              Create First Assessment
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {assessments.map((assessment) => (
              <div
                key={assessment.id}
                className="card flex items-center justify-between"
              >
                <div>
                  <p className="font-medium text-gray-900">
                    Assessment - {formatDate(assessment.assessment_date)}
                  </p>
                  <p className="text-sm text-gray-600">
                    FMS Score: {assessment.fms_scores?.total_score || "N/A"}/21
                  </p>
                </div>
                <div className="flex gap-2">
                  <Link
                    href={`/clients/${clientId}/assessment/${assessment.id}/generate`}
                    className="btn-primary text-sm flex items-center gap-1"
                  >
                    <Sparkles className="h-4 w-4" />
                    Generate Plan
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Workout Plans */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Workout Plans</h2>
        </div>

        {plans.length === 0 ? (
          <div className="card text-center py-8">
            <Calendar className="h-8 w-8 text-gray-400 mx-auto mb-2" />
            <p className="text-gray-600">No workout plans yet</p>
            <p className="text-sm text-gray-500 mt-1">
              Create an assessment first, then generate a plan
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {plans.map((plan) => (
              <Link
                key={plan.id}
                href={`/plans/${plan.id}`}
                className="card flex items-center justify-between hover:shadow-md transition-shadow"
              >
                <div>
                  <p className="font-medium text-gray-900">{plan.name}</p>
                  <p className="text-sm text-gray-600">
                    {plan.weeks} weeks starting {formatDate(plan.start_date)}
                  </p>
                </div>
                <span
                  className={`rounded-full px-3 py-1 text-xs font-medium ${
                    plan.status === "active"
                      ? "bg-green-100 text-green-700"
                      : plan.status === "completed"
                      ? "bg-gray-100 text-gray-700"
                      : "bg-yellow-100 text-yellow-700"
                  }`}
                >
                  {plan.status}
                </span>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
