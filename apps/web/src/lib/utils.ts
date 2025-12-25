import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date): string {
  return new Date(date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function extractYouTubeId(url: string): string | null {
  const regex =
    /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
  const match = url.match(regex);
  return match ? match[1] : null;
}

export function getYouTubeThumbnail(url: string): string | null {
  const videoId = extractYouTubeId(url);
  return videoId ? `https://img.youtube.com/vi/${videoId}/mqdefault.jpg` : null;
}

export function calculateBMI(weightKg: number, heightCm: number): number {
  const heightM = heightCm / 100;
  return Number((weightKg / (heightM * heightM)).toFixed(1));
}

export function calculateFMSTotal(scores: {
  deep_squat: number;
  hurdle_step: number;
  inline_lunge: number;
  shoulder_mobility: number;
  active_straight_leg_raise: number;
  trunk_stability_pushup: number;
  rotary_stability: number;
}): number {
  return Object.values(scores).reduce((sum, score) => sum + score, 0);
}

export function getFMSRiskLevel(totalScore: number): {
  level: "low" | "moderate" | "high";
  label: string;
  color: string;
} {
  if (totalScore >= 15) {
    return { level: "low", label: "Low Risk", color: "text-green-600" };
  } else if (totalScore >= 12) {
    return { level: "moderate", label: "Moderate Risk", color: "text-yellow-600" };
  } else {
    return { level: "high", label: "High Risk", color: "text-red-600" };
  }
}

export const DAYS_OF_WEEK = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
];

export const EQUIPMENT_OPTIONS = [
  "Barbell",
  "Dumbbells",
  "Kettlebells",
  "Resistance Bands",
  "Pull-up Bar",
  "Bench",
  "Cable Machine",
  "Squat Rack",
  "Treadmill",
  "Rowing Machine",
  "Bike",
  "Medicine Ball",
  "Foam Roller",
  "Yoga Mat",
  "None (Bodyweight)",
];

export const EXERCISE_CATEGORIES = [
  { value: "strength", label: "Strength" },
  { value: "cardio", label: "Cardio" },
  { value: "mobility", label: "Mobility" },
  { value: "flexibility", label: "Flexibility" },
  { value: "balance", label: "Balance" },
  { value: "plyometric", label: "Plyometric" },
  { value: "core", label: "Core" },
  { value: "warm_up", label: "Warm Up" },
  { value: "cool_down", label: "Cool Down" },
];

export const PRIORITY_FOCUS_OPTIONS = [
  { value: "fat_loss", label: "Fat Loss" },
  { value: "muscle_gain", label: "Muscle Gain" },
  { value: "strength", label: "Strength" },
  { value: "endurance", label: "Endurance" },
  { value: "flexibility", label: "Flexibility" },
  { value: "mobility", label: "Mobility" },
  { value: "sports_performance", label: "Sports Performance" },
  { value: "general_fitness", label: "General Fitness" },
  { value: "injury_rehab", label: "Injury Rehab" },
];
