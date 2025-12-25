import { createClient } from "@/lib/supabase/server";
import { Library, Users, Calendar, TrendingUp } from "lucide-react";
import Link from "next/link";

export default async function DashboardPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  const userName = user?.user_metadata?.name || "Coach";

  // In production, these would come from API calls
  const stats = [
    {
      name: "Total Exercises",
      value: "0",
      icon: Library,
      href: "/exercises",
      color: "bg-primary-100 text-primary-600",
    },
    {
      name: "Active Clients",
      value: "0",
      icon: Users,
      href: "/clients",
      color: "bg-accent-100 text-accent-600",
    },
    {
      name: "Workout Plans",
      value: "0",
      icon: Calendar,
      href: "/plans",
      color: "bg-green-100 text-green-600",
    },
    {
      name: "Assessments",
      value: "0",
      icon: TrendingUp,
      href: "/clients",
      color: "bg-yellow-100 text-yellow-600",
    },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {userName}!
        </h1>
        <p className="mt-1 text-gray-600">
          Here&apos;s an overview of your coaching platform
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Link key={stat.name} href={stat.href} className="card hover:shadow-md transition-shadow">
            <div className="flex items-center gap-4">
              <div className={`rounded-lg p-3 ${stat.color}`}>
                <stat.icon className="h-6 w-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="mt-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Quick Actions
        </h2>
        <div className="grid gap-4 sm:grid-cols-3">
          <Link
            href="/exercises/new"
            className="card hover:shadow-md transition-shadow flex items-center gap-3"
          >
            <div className="rounded-lg bg-primary-100 p-2">
              <Library className="h-5 w-5 text-primary-600" />
            </div>
            <div>
              <p className="font-medium text-gray-900">Add Exercise</p>
              <p className="text-sm text-gray-600">
                Add a new exercise to your library
              </p>
            </div>
          </Link>

          <Link
            href="/clients/new"
            className="card hover:shadow-md transition-shadow flex items-center gap-3"
          >
            <div className="rounded-lg bg-accent-100 p-2">
              <Users className="h-5 w-5 text-accent-600" />
            </div>
            <div>
              <p className="font-medium text-gray-900">Add Client</p>
              <p className="text-sm text-gray-600">
                Register a new client
              </p>
            </div>
          </Link>

          <Link
            href="/plans/new"
            className="card hover:shadow-md transition-shadow flex items-center gap-3"
          >
            <div className="rounded-lg bg-green-100 p-2">
              <Calendar className="h-5 w-5 text-green-600" />
            </div>
            <div>
              <p className="font-medium text-gray-900">Create Plan</p>
              <p className="text-sm text-gray-600">
                Generate a new workout plan
              </p>
            </div>
          </Link>
        </div>
      </div>

      {/* Getting Started */}
      <div className="mt-8 card bg-gradient-to-r from-primary-500 to-accent-500 text-white">
        <h2 className="text-xl font-bold">Getting Started</h2>
        <p className="mt-2 text-primary-100">
          Welcome to Coach Platform! Start by adding exercises to your library,
          then register your clients and create personalized workout plans.
        </p>
        <div className="mt-4 flex gap-3">
          <Link
            href="/exercises"
            className="rounded-lg bg-white px-4 py-2 text-sm font-medium text-primary-600 hover:bg-primary-50 transition-colors"
          >
            Go to Exercises
          </Link>
        </div>
      </div>
    </div>
  );
}
