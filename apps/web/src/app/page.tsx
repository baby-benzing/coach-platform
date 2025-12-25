import Link from "next/link";
import { Dumbbell, Users, Calendar, Zap } from "lucide-react";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-accent-50">
      {/* Navigation */}
      <nav className="border-b bg-white/80 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-2">
              <Dumbbell className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">
                Coach Platform
              </span>
            </div>
            <div className="flex items-center gap-4">
              <Link
                href="/login"
                className="text-sm font-medium text-gray-700 hover:text-primary-600"
              >
                Log in
              </Link>
              <Link href="/signup" className="btn-primary">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            Streamline Your
            <span className="text-primary-600"> Coaching</span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            Build exercise libraries, assess clients, and generate personalized
            workout plans with AI-powered insights. All in one place.
          </p>
          <div className="mt-10 flex items-center justify-center gap-4">
            <Link href="/signup" className="btn-primary text-lg px-8 py-3">
              Start Free Trial
            </Link>
            <Link
              href="#features"
              className="btn-secondary text-lg px-8 py-3"
            >
              Learn More
            </Link>
          </div>
        </div>

        {/* Features */}
        <div id="features" className="mt-32 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          <div className="card text-center">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100">
              <Dumbbell className="h-6 w-6 text-primary-600" />
            </div>
            <h3 className="mt-4 text-lg font-semibold text-gray-900">
              Exercise Library
            </h3>
            <p className="mt-2 text-sm text-gray-600">
              Build and organize your exercise database with AI-enhanced tagging
            </p>
          </div>

          <div className="card text-center">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-lg bg-accent-100">
              <Users className="h-6 w-6 text-accent-600" />
            </div>
            <h3 className="mt-4 text-lg font-semibold text-gray-900">
              Client Management
            </h3>
            <p className="mt-2 text-sm text-gray-600">
              Track assessments, progress, and history for each client
            </p>
          </div>

          <div className="card text-center">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-lg bg-green-100">
              <Calendar className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="mt-4 text-lg font-semibold text-gray-900">
              Workout Plans
            </h3>
            <p className="mt-2 text-sm text-gray-600">
              Create periodized 4-week programs tailored to each client
            </p>
          </div>

          <div className="card text-center">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-lg bg-yellow-100">
              <Zap className="h-6 w-6 text-yellow-600" />
            </div>
            <h3 className="mt-4 text-lg font-semibold text-gray-900">
              AI-Powered
            </h3>
            <p className="mt-2 text-sm text-gray-600">
              Generate intelligent workout suggestions based on assessments
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t bg-white py-8">
        <div className="mx-auto max-w-7xl px-4 text-center text-sm text-gray-500">
          <p>&copy; 2025 Coach Platform. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
