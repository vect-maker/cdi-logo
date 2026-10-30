import { z } from "zod";

export const FigureIdSchema = z.enum([
  "c1-tesseract",
  "c2-matrix",
  "c3-circuit",
  "c4-network",
  "c5-binary",
  "c6-waveform",
]);

export const PaletteIdSchema = z.enum([
  "light",
  "dark",
  "cobalt",
  "emerald",
  "violet",
  "amber",
]);

export const PositionIdSchema = z.enum([
  "chest-center",
  "chest-left",
  "sleeve-left",
  "back-collar",
]);

export const StudentIdSchema = z
  .string()
  .trim()
  .regex(/^\d{8}$/, "El carné debe tener exactamente 8 dígitos numéricos (ej. 20260001)");

export const StudentNameSchema = z
  .string()
  .trim()
  .min(3, "El nombre debe contener al menos 3 caracteres")
  .max(100, "El nombre no puede exceder 100 caracteres");
