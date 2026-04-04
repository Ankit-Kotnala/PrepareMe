"use client";

import { create } from "zustand";

export type AppRole =
  | "student"
  | "teacher"
  | "course_admin"
  | "institution_admin"
  | "platform_admin";

type SessionState = {
  role: AppRole;
  institutionName: string;
  setRole: (role: AppRole) => void;
  setInstitutionName: (institutionName: string) => void;
};

export const useSessionStore = create<SessionState>((set) => ({
  role: "teacher",
  institutionName: "PrepareMe Demo Institution",
  setRole: (role) => set({ role }),
  setInstitutionName: (institutionName) => set({ institutionName })
}));

