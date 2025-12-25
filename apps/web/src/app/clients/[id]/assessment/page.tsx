"use client";

import { useState } from "react";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Loader2, ChevronRight, ChevronLeft } from "lucide-react";
import { createClient } from "@/lib/supabase/client";
import {
  EQUIPMENT_OPTIONS,
  PRIORITY_FOCUS_OPTIONS,
  DAYS_OF_WEEK,
  calculateBMI,
  calculateFMSTotal,
} from "@/lib/utils";
import type {
  PersonalInfo,
  BodyMetrics,
  HealthHistory,
  InjuryInfo,
  FitnessGoals,
  ExerciseHistoryData,
  LifestyleInfo,
  AvailabilityInfo,
  StrengthBaseline,
  CardioBaseline,
  FMSScores,
  PriorityFocus,
} from "@/types";

const STEPS = [
  "Personal Info",
  "Body Metrics",
  "Health History",
  "Injuries",
  "Goals",
  "Exercise History",
  "Lifestyle",
  "Availability",
  "Strength",
  "Cardio",
  "FMS Assessment",
];

export default function AssessmentPage() {
  const router = useRouter();
  const params = useParams();
  const clientId = params.id as string;

  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Form state for each section
  const [personalInfo, setPersonalInfo] = useState<PersonalInfo>({
    emergency_contact_name: "",
    emergency_contact_phone: "",
    occupation: "",
  });

  const [bodyMetrics, setBodyMetrics] = useState<BodyMetrics>({
    height_cm: 170,
    weight_kg: 70,
    body_fat_percentage: undefined,
  });

  const [healthHistory, setHealthHistory] = useState<HealthHistory>({
    medical_conditions: [],
    medications: [],
    surgeries: [],
    allergies: [],
  });

  const [injuries, setInjuries] = useState<InjuryInfo>({
    past_injuries: [],
    current_limitations: [],
    pain_areas: [],
  });

  const [fitnessGoals, setFitnessGoals] = useState<FitnessGoals>({
    short_term: "",
    long_term: "",
    priority_focus: [],
  });

  const [exerciseHistory, setExerciseHistory] = useState<ExerciseHistoryData>({
    experience_level: "beginner",
    current_frequency: 0,
    past_sports: [],
    current_activities: [],
  });

  const [lifestyle, setLifestyle] = useState<LifestyleInfo>({
    sleep_hours: 7,
    sleep_quality: "good",
    stress_level: "moderate",
    diet_type: "",
    hydration_liters: 2,
  });

  const [availability, setAvailability] = useState<AvailabilityInfo>({
    days_per_week: 3,
    minutes_per_session: 60,
    preferred_days: [],
    equipment_access: [],
    training_location: "gym",
  });

  const [strengthBaseline, setStrengthBaseline] = useState<StrengthBaseline>({
    squat_1rm_kg: undefined,
    bench_1rm_kg: undefined,
    deadlift_1rm_kg: undefined,
    push_up_max: undefined,
    pull_up_max: undefined,
    plank_hold_seconds: undefined,
  });

  const [cardioBaseline, setCardioBaseline] = useState<CardioBaseline>({
    resting_hr: undefined,
    max_hr: undefined,
    estimated_vo2max: undefined,
    run_5k_minutes: undefined,
    run_1mile_minutes: undefined,
  });

  const [fmsScores, setFmsScores] = useState<Omit<FMSScores, "total_score">>({
    deep_squat: 2,
    hurdle_step: 2,
    inline_lunge: 2,
    shoulder_mobility: 2,
    active_straight_leg_raise: 2,
    trunk_stability_pushup: 2,
    rotary_stability: 2,
  });

  const [customFields, setCustomFields] = useState<Record<string, string>>({});
  const [newCustomFieldKey, setNewCustomFieldKey] = useState("");
  const [newCustomFieldValue, setNewCustomFieldValue] = useState("");

  const addListItem = (
    setter: React.Dispatch<React.SetStateAction<string[]>>,
    list: string[],
    value: string
  ) => {
    if (value.trim() && !list.includes(value.trim())) {
      setter([...list, value.trim()]);
    }
  };

  const removeListItem = (
    setter: React.Dispatch<React.SetStateAction<string[]>>,
    list: string[],
    value: string
  ) => {
    setter(list.filter((item) => item !== value));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError("");

    try {
      const supabase = createClient();
      const { data: { session } } = await supabase.auth.getSession();

      if (!session) {
        throw new Error("Not authenticated");
      }

      const assessmentData = {
        assessment_date: new Date().toISOString(),
        personal_info: personalInfo,
        body_metrics: bodyMetrics,
        health_history: healthHistory,
        injuries,
        fitness_goals: fitnessGoals,
        exercise_history: exerciseHistory,
        lifestyle,
        availability,
        strength_baseline: strengthBaseline,
        cardio_baseline: cardioBaseline,
        fms_scores: {
          ...fmsScores,
          total_score: calculateFMSTotal(fmsScores),
        },
        custom_fields: customFields,
      };

      const response = await fetch(`/api/v1/clients/${clientId}/assessments`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session.access_token}`,
        },
        body: JSON.stringify(assessmentData),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Failed to save assessment");
      }

      router.push(`/clients/${clientId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 0: // Personal Info
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-900">Emergency Contact & Personal Details</h3>
            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label className="label">Emergency Contact Name</label>
                <input
                  type="text"
                  value={personalInfo.emergency_contact_name}
                  onChange={(e) =>
                    setPersonalInfo({ ...personalInfo, emergency_contact_name: e.target.value })
                  }
                  className="input mt-1"
                  placeholder="Jane Doe"
                />
              </div>
              <div>
                <label className="label">Emergency Contact Phone</label>
                <input
                  type="tel"
                  value={personalInfo.emergency_contact_phone}
                  onChange={(e) =>
                    setPersonalInfo({ ...personalInfo, emergency_contact_phone: e.target.value })
                  }
                  className="input mt-1"
                  placeholder="+1 (555) 123-4567"
                />
              </div>
            </div>
            <div>
              <label className="label">Occupation</label>
              <input
                type="text"
                value={personalInfo.occupation}
                onChange={(e) =>
                  setPersonalInfo({ ...personalInfo, occupation: e.target.value })
                }
                className="input mt-1"
                placeholder="Software Engineer"
              />
              <p className="mt-1 text-xs text-gray-500">
                Helps understand daily activity level and potential repetitive stress
              </p>
            </div>
          </div>
        );

      case 1: // Body Metrics
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-900">Body Measurements</h3>
            <div className="grid gap-4 sm:grid-cols-3">
              <div>
                <label className="label">Height (cm)</label>
                <input
                  type="number"
                  value={bodyMetrics.height_cm}
                  onChange={(e) =>
                    setBodyMetrics({ ...bodyMetrics, height_cm: Number(e.target.value) })
                  }
                  className="input mt-1"
                  min={100}
                  max={250}
                />
              </div>
              <div>
                <label className="label">Weight (kg)</label>
                <input
                  type="number"
                  value={bodyMetrics.weight_kg}
                  onChange={(e) =>
                    setBodyMetrics({ ...bodyMetrics, weight_kg: Number(e.target.value) })
                  }
                  className="input mt-1"
                  min={30}
                  max={300}
                />
              </div>
              <div>
                <label className="label">Body Fat % (optional)</label>
                <input
                  type="number"
                  value={bodyMetrics.body_fat_percentage || ""}
                  onChange={(e) =>
                    setBodyMetrics({
                      ...bodyMetrics,
                      body_fat_percentage: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  className="input mt-1"
                  min={3}
                  max={60}
                />
              </div>
            </div>
            <div className="rounded-lg bg-gray-50 p-4">
              <p className="text-sm text-gray-600">
                Calculated BMI:{" "}
                <span className="font-semibold">
                  {calculateBMI(bodyMetrics.weight_kg, bodyMetrics.height_cm)}
                </span>
              </p>
            </div>
          </div>
        );

      case 2: // Health History
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900">Health & Medical History</h3>

            <ArrayInput
              label="Medical Conditions"
              placeholder="e.g., Hypertension, Diabetes"
              items={healthHistory.medical_conditions}
              onAdd={(value) =>
                setHealthHistory({
                  ...healthHistory,
                  medical_conditions: [...healthHistory.medical_conditions, value],
                })
              }
              onRemove={(value) =>
                setHealthHistory({
                  ...healthHistory,
                  medical_conditions: healthHistory.medical_conditions.filter((i) => i !== value),
                })
              }
            />

            <ArrayInput
              label="Current Medications"
              placeholder="e.g., Metformin 500mg"
              items={healthHistory.medications}
              onAdd={(value) =>
                setHealthHistory({
                  ...healthHistory,
                  medications: [...healthHistory.medications, value],
                })
              }
              onRemove={(value) =>
                setHealthHistory({
                  ...healthHistory,
                  medications: healthHistory.medications.filter((i) => i !== value),
                })
              }
            />

            <ArrayInput
              label="Past Surgeries"
              placeholder="e.g., ACL repair (2020)"
              items={healthHistory.surgeries}
              onAdd={(value) =>
                setHealthHistory({
                  ...healthHistory,
                  surgeries: [...healthHistory.surgeries, value],
                })
              }
              onRemove={(value) =>
                setHealthHistory({
                  ...healthHistory,
                  surgeries: healthHistory.surgeries.filter((i) => i !== value),
                })
              }
            />

            <ArrayInput
              label="Allergies"
              placeholder="e.g., Latex, Penicillin"
              items={healthHistory.allergies}
              onAdd={(value) =>
                setHealthHistory({
                  ...healthHistory,
                  allergies: [...healthHistory.allergies, value],
                })
              }
              onRemove={(value) =>
                setHealthHistory({
                  ...healthHistory,
                  allergies: healthHistory.allergies.filter((i) => i !== value),
                })
              }
            />
          </div>
        );

      case 3: // Injuries
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900">Injuries & Limitations</h3>

            <ArrayInput
              label="Past Injuries"
              placeholder="e.g., Sprained ankle (2019)"
              items={injuries.past_injuries}
              onAdd={(value) =>
                setInjuries({ ...injuries, past_injuries: [...injuries.past_injuries, value] })
              }
              onRemove={(value) =>
                setInjuries({
                  ...injuries,
                  past_injuries: injuries.past_injuries.filter((i) => i !== value),
                })
              }
            />

            <ArrayInput
              label="Current Limitations"
              placeholder="e.g., Limited overhead mobility"
              items={injuries.current_limitations}
              onAdd={(value) =>
                setInjuries({
                  ...injuries,
                  current_limitations: [...injuries.current_limitations, value],
                })
              }
              onRemove={(value) =>
                setInjuries({
                  ...injuries,
                  current_limitations: injuries.current_limitations.filter((i) => i !== value),
                })
              }
            />

            <ArrayInput
              label="Pain Areas"
              placeholder="e.g., Lower back, Right knee"
              items={injuries.pain_areas}
              onAdd={(value) =>
                setInjuries({ ...injuries, pain_areas: [...injuries.pain_areas, value] })
              }
              onRemove={(value) =>
                setInjuries({
                  ...injuries,
                  pain_areas: injuries.pain_areas.filter((i) => i !== value),
                })
              }
            />
          </div>
        );

      case 4: // Goals
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900">Fitness Goals</h3>

            <div>
              <label className="label">Short-term Goal (3 months)</label>
              <textarea
                value={fitnessGoals.short_term}
                onChange={(e) =>
                  setFitnessGoals({ ...fitnessGoals, short_term: e.target.value })
                }
                className="input mt-1 min-h-[80px]"
                placeholder="What do you want to achieve in the next 3 months?"
              />
            </div>

            <div>
              <label className="label">Long-term Goal (1 year)</label>
              <textarea
                value={fitnessGoals.long_term}
                onChange={(e) =>
                  setFitnessGoals({ ...fitnessGoals, long_term: e.target.value })
                }
                className="input mt-1 min-h-[80px]"
                placeholder="Where do you want to be in 1 year?"
              />
            </div>

            <div>
              <label className="label">Priority Focus Areas</label>
              <div className="mt-2 flex flex-wrap gap-2">
                {PRIORITY_FOCUS_OPTIONS.map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    onClick={() => {
                      const focus = option.value as PriorityFocus;
                      setFitnessGoals({
                        ...fitnessGoals,
                        priority_focus: fitnessGoals.priority_focus.includes(focus)
                          ? fitnessGoals.priority_focus.filter((f) => f !== focus)
                          : [...fitnessGoals.priority_focus, focus],
                      });
                    }}
                    className={`rounded-full px-3 py-1 text-sm transition-colors ${
                      fitnessGoals.priority_focus.includes(option.value as PriorityFocus)
                        ? "bg-primary-600 text-white"
                        : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        );

      case 5: // Exercise History
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900">Exercise Background</h3>

            <div>
              <label className="label">Experience Level</label>
              <select
                value={exerciseHistory.experience_level}
                onChange={(e) =>
                  setExerciseHistory({
                    ...exerciseHistory,
                    experience_level: e.target.value as "beginner" | "intermediate" | "advanced",
                  })
                }
                className="input mt-1"
              >
                <option value="beginner">Beginner (0-1 years)</option>
                <option value="intermediate">Intermediate (1-3 years)</option>
                <option value="advanced">Advanced (3+ years)</option>
              </select>
            </div>

            <div>
              <label className="label">Current Training Frequency (days/week)</label>
              <input
                type="number"
                value={exerciseHistory.current_frequency}
                onChange={(e) =>
                  setExerciseHistory({
                    ...exerciseHistory,
                    current_frequency: Number(e.target.value),
                  })
                }
                className="input mt-1"
                min={0}
                max={7}
              />
            </div>

            <ArrayInput
              label="Past Sports"
              placeholder="e.g., Soccer, Swimming"
              items={exerciseHistory.past_sports}
              onAdd={(value) =>
                setExerciseHistory({
                  ...exerciseHistory,
                  past_sports: [...exerciseHistory.past_sports, value],
                })
              }
              onRemove={(value) =>
                setExerciseHistory({
                  ...exerciseHistory,
                  past_sports: exerciseHistory.past_sports.filter((i) => i !== value),
                })
              }
            />

            <ArrayInput
              label="Current Activities"
              placeholder="e.g., Running, Yoga"
              items={exerciseHistory.current_activities}
              onAdd={(value) =>
                setExerciseHistory({
                  ...exerciseHistory,
                  current_activities: [...exerciseHistory.current_activities, value],
                })
              }
              onRemove={(value) =>
                setExerciseHistory({
                  ...exerciseHistory,
                  current_activities: exerciseHistory.current_activities.filter((i) => i !== value),
                })
              }
            />
          </div>
        );

      case 6: // Lifestyle
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900">Lifestyle Factors</h3>

            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label className="label">Average Sleep (hours/night)</label>
                <input
                  type="number"
                  value={lifestyle.sleep_hours}
                  onChange={(e) =>
                    setLifestyle({ ...lifestyle, sleep_hours: Number(e.target.value) })
                  }
                  className="input mt-1"
                  min={3}
                  max={12}
                  step={0.5}
                />
              </div>

              <div>
                <label className="label">Sleep Quality</label>
                <select
                  value={lifestyle.sleep_quality}
                  onChange={(e) =>
                    setLifestyle({
                      ...lifestyle,
                      sleep_quality: e.target.value as LifestyleInfo["sleep_quality"],
                    })
                  }
                  className="input mt-1"
                >
                  <option value="poor">Poor</option>
                  <option value="fair">Fair</option>
                  <option value="good">Good</option>
                  <option value="excellent">Excellent</option>
                </select>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label className="label">Stress Level</label>
                <select
                  value={lifestyle.stress_level}
                  onChange={(e) =>
                    setLifestyle({
                      ...lifestyle,
                      stress_level: e.target.value as LifestyleInfo["stress_level"],
                    })
                  }
                  className="input mt-1"
                >
                  <option value="low">Low</option>
                  <option value="moderate">Moderate</option>
                  <option value="high">High</option>
                  <option value="very_high">Very High</option>
                </select>
              </div>

              <div>
                <label className="label">Daily Hydration (liters)</label>
                <input
                  type="number"
                  value={lifestyle.hydration_liters}
                  onChange={(e) =>
                    setLifestyle({ ...lifestyle, hydration_liters: Number(e.target.value) })
                  }
                  className="input mt-1"
                  min={0}
                  max={10}
                  step={0.5}
                />
              </div>
            </div>

            <div>
              <label className="label">Diet Type</label>
              <input
                type="text"
                value={lifestyle.diet_type}
                onChange={(e) => setLifestyle({ ...lifestyle, diet_type: e.target.value })}
                className="input mt-1"
                placeholder="e.g., Balanced, Vegetarian, Keto"
              />
            </div>
          </div>
        );

      case 7: // Availability
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900">Training Availability</h3>

            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label className="label">Days per Week</label>
                <input
                  type="number"
                  value={availability.days_per_week}
                  onChange={(e) =>
                    setAvailability({ ...availability, days_per_week: Number(e.target.value) })
                  }
                  className="input mt-1"
                  min={1}
                  max={7}
                />
              </div>

              <div>
                <label className="label">Minutes per Session</label>
                <input
                  type="number"
                  value={availability.minutes_per_session}
                  onChange={(e) =>
                    setAvailability({
                      ...availability,
                      minutes_per_session: Number(e.target.value),
                    })
                  }
                  className="input mt-1"
                  min={15}
                  max={180}
                  step={15}
                />
              </div>
            </div>

            <div>
              <label className="label">Preferred Training Days</label>
              <div className="mt-2 flex flex-wrap gap-2">
                {DAYS_OF_WEEK.map((day) => (
                  <button
                    key={day}
                    type="button"
                    onClick={() => {
                      setAvailability({
                        ...availability,
                        preferred_days: availability.preferred_days.includes(day)
                          ? availability.preferred_days.filter((d) => d !== day)
                          : [...availability.preferred_days, day],
                      });
                    }}
                    className={`rounded-full px-3 py-1 text-sm transition-colors ${
                      availability.preferred_days.includes(day)
                        ? "bg-primary-600 text-white"
                        : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                    }`}
                  >
                    {day}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="label">Training Location</label>
              <select
                value={availability.training_location}
                onChange={(e) =>
                  setAvailability({
                    ...availability,
                    training_location: e.target.value as AvailabilityInfo["training_location"],
                  })
                }
                className="input mt-1"
              >
                <option value="gym">Gym</option>
                <option value="home">Home</option>
                <option value="outdoor">Outdoor</option>
                <option value="hybrid">Hybrid</option>
              </select>
            </div>

            <div>
              <label className="label">Available Equipment</label>
              <div className="mt-2 flex flex-wrap gap-2">
                {EQUIPMENT_OPTIONS.map((equipment) => (
                  <button
                    key={equipment}
                    type="button"
                    onClick={() => {
                      setAvailability({
                        ...availability,
                        equipment_access: availability.equipment_access.includes(equipment)
                          ? availability.equipment_access.filter((e) => e !== equipment)
                          : [...availability.equipment_access, equipment],
                      });
                    }}
                    className={`rounded-full px-3 py-1 text-sm transition-colors ${
                      availability.equipment_access.includes(equipment)
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
        );

      case 8: // Strength
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900">Strength Baseline</h3>
            <p className="text-sm text-gray-600">
              Enter estimated 1RM or best recent lifts (optional)
            </p>

            <div className="grid gap-4 sm:grid-cols-3">
              <div>
                <label className="label">Squat 1RM (kg)</label>
                <input
                  type="number"
                  value={strengthBaseline.squat_1rm_kg || ""}
                  onChange={(e) =>
                    setStrengthBaseline({
                      ...strengthBaseline,
                      squat_1rm_kg: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  className="input mt-1"
                />
              </div>
              <div>
                <label className="label">Bench 1RM (kg)</label>
                <input
                  type="number"
                  value={strengthBaseline.bench_1rm_kg || ""}
                  onChange={(e) =>
                    setStrengthBaseline({
                      ...strengthBaseline,
                      bench_1rm_kg: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  className="input mt-1"
                />
              </div>
              <div>
                <label className="label">Deadlift 1RM (kg)</label>
                <input
                  type="number"
                  value={strengthBaseline.deadlift_1rm_kg || ""}
                  onChange={(e) =>
                    setStrengthBaseline({
                      ...strengthBaseline,
                      deadlift_1rm_kg: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  className="input mt-1"
                />
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-3">
              <div>
                <label className="label">Push-up Max</label>
                <input
                  type="number"
                  value={strengthBaseline.push_up_max || ""}
                  onChange={(e) =>
                    setStrengthBaseline({
                      ...strengthBaseline,
                      push_up_max: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  className="input mt-1"
                />
              </div>
              <div>
                <label className="label">Pull-up Max</label>
                <input
                  type="number"
                  value={strengthBaseline.pull_up_max || ""}
                  onChange={(e) =>
                    setStrengthBaseline({
                      ...strengthBaseline,
                      pull_up_max: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  className="input mt-1"
                />
              </div>
              <div>
                <label className="label">Plank Hold (seconds)</label>
                <input
                  type="number"
                  value={strengthBaseline.plank_hold_seconds || ""}
                  onChange={(e) =>
                    setStrengthBaseline({
                      ...strengthBaseline,
                      plank_hold_seconds: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  className="input mt-1"
                />
              </div>
            </div>
          </div>
        );

      case 9: // Cardio
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900">Cardio Baseline</h3>

            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label className="label">Resting Heart Rate (bpm)</label>
                <input
                  type="number"
                  value={cardioBaseline.resting_hr || ""}
                  onChange={(e) =>
                    setCardioBaseline({
                      ...cardioBaseline,
                      resting_hr: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  className="input mt-1"
                />
              </div>
              <div>
                <label className="label">Max Heart Rate (bpm)</label>
                <input
                  type="number"
                  value={cardioBaseline.max_hr || ""}
                  onChange={(e) =>
                    setCardioBaseline({
                      ...cardioBaseline,
                      max_hr: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  className="input mt-1"
                />
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-3">
              <div>
                <label className="label">Estimated VO2max</label>
                <input
                  type="number"
                  value={cardioBaseline.estimated_vo2max || ""}
                  onChange={(e) =>
                    setCardioBaseline({
                      ...cardioBaseline,
                      estimated_vo2max: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  className="input mt-1"
                />
              </div>
              <div>
                <label className="label">5K Time (minutes)</label>
                <input
                  type="number"
                  value={cardioBaseline.run_5k_minutes || ""}
                  onChange={(e) =>
                    setCardioBaseline({
                      ...cardioBaseline,
                      run_5k_minutes: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  className="input mt-1"
                />
              </div>
              <div>
                <label className="label">1 Mile Time (minutes)</label>
                <input
                  type="number"
                  value={cardioBaseline.run_1mile_minutes || ""}
                  onChange={(e) =>
                    setCardioBaseline({
                      ...cardioBaseline,
                      run_1mile_minutes: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  className="input mt-1"
                  step={0.1}
                />
              </div>
            </div>
          </div>
        );

      case 10: // FMS
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium text-gray-900">
              Functional Movement Screen (FMS)
            </h3>
            <p className="text-sm text-gray-600">
              Score each movement from 0-3. Total score below 14 indicates higher injury risk.
            </p>

            <div className="space-y-4">
              {[
                { key: "deep_squat", label: "Deep Squat" },
                { key: "hurdle_step", label: "Hurdle Step" },
                { key: "inline_lunge", label: "Inline Lunge" },
                { key: "shoulder_mobility", label: "Shoulder Mobility" },
                { key: "active_straight_leg_raise", label: "Active Straight Leg Raise" },
                { key: "trunk_stability_pushup", label: "Trunk Stability Push-up" },
                { key: "rotary_stability", label: "Rotary Stability" },
              ].map(({ key, label }) => (
                <div key={key} className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">{label}</span>
                  <div className="flex gap-2">
                    {[0, 1, 2, 3].map((score) => (
                      <button
                        key={score}
                        type="button"
                        onClick={() =>
                          setFmsScores({ ...fmsScores, [key]: score })
                        }
                        className={`h-10 w-10 rounded-lg font-medium transition-colors ${
                          fmsScores[key as keyof typeof fmsScores] === score
                            ? "bg-primary-600 text-white"
                            : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                        }`}
                      >
                        {score}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div className="rounded-lg bg-gray-50 p-4">
              <div className="flex items-center justify-between">
                <span className="font-medium text-gray-900">Total Score</span>
                <span
                  className={`text-2xl font-bold ${
                    calculateFMSTotal(fmsScores) >= 14
                      ? "text-green-600"
                      : calculateFMSTotal(fmsScores) >= 12
                      ? "text-yellow-600"
                      : "text-red-600"
                  }`}
                >
                  {calculateFMSTotal(fmsScores)} / 21
                </span>
              </div>
              <p className="mt-1 text-sm text-gray-600">
                {calculateFMSTotal(fmsScores) >= 14
                  ? "Low injury risk"
                  : calculateFMSTotal(fmsScores) >= 12
                  ? "Moderate injury risk"
                  : "Higher injury risk - consider corrective exercises"}
              </p>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="max-w-3xl">
      <div className="mb-8">
        <Link
          href={`/clients/${clientId}`}
          className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Client
        </Link>
        <h1 className="mt-4 text-2xl font-bold text-gray-900">New Assessment</h1>
        <p className="mt-1 text-gray-600">
          Complete the assessment to generate personalized workout plans
        </p>
      </div>

      {/* Progress */}
      <div className="mb-8">
        <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
          <span>
            Step {currentStep + 1} of {STEPS.length}
          </span>
          <span>{STEPS[currentStep]}</span>
        </div>
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-primary-600 transition-all duration-300"
            style={{ width: `${((currentStep + 1) / STEPS.length) * 100}%` }}
          />
        </div>
      </div>

      {error && (
        <div className="mb-6 rounded-lg bg-red-50 p-4 text-sm text-red-600">
          {error}
        </div>
      )}

      <div className="card mb-6">{renderStepContent()}</div>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <button
          type="button"
          onClick={() => setCurrentStep(currentStep - 1)}
          disabled={currentStep === 0}
          className="btn-secondary flex items-center gap-2 disabled:opacity-50"
        >
          <ChevronLeft className="h-4 w-4" />
          Previous
        </button>

        {currentStep === STEPS.length - 1 ? (
          <button
            type="button"
            onClick={handleSubmit}
            disabled={loading}
            className="btn-primary flex items-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Saving...
              </>
            ) : (
              "Save Assessment"
            )}
          </button>
        ) : (
          <button
            type="button"
            onClick={() => setCurrentStep(currentStep + 1)}
            className="btn-primary flex items-center gap-2"
          >
            Next
            <ChevronRight className="h-4 w-4" />
          </button>
        )}
      </div>
    </div>
  );
}

// Helper component for array inputs
function ArrayInput({
  label,
  placeholder,
  items,
  onAdd,
  onRemove,
}: {
  label: string;
  placeholder: string;
  items: string[];
  onAdd: (value: string) => void;
  onRemove: (value: string) => void;
}) {
  const [value, setValue] = useState("");

  const handleAdd = () => {
    if (value.trim()) {
      onAdd(value.trim());
      setValue("");
    }
  };

  return (
    <div>
      <label className="label">{label}</label>
      <div className="mt-1 flex gap-2">
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              handleAdd();
            }
          }}
          className="input flex-1"
          placeholder={placeholder}
        />
        <button type="button" onClick={handleAdd} className="btn-secondary">
          Add
        </button>
      </div>
      {items.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-2">
          {items.map((item) => (
            <span
              key={item}
              className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-3 py-1 text-sm"
            >
              {item}
              <button
                type="button"
                onClick={() => onRemove(item)}
                className="text-gray-500 hover:text-gray-700"
              >
                &times;
              </button>
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
