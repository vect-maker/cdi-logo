import { z } from "zod";
import {
  FigureIdSchema,
  PaletteIdSchema,
  PositionIdSchema,
  StudentIdSchema,
  StudentNameSchema,
} from "./domain";

export const CheckStudentRequestSchema = z.object({
  student_id: StudentIdSchema,
});

export const SubmitVoteRequestSchema = z.object({
  student_id: StudentIdSchema,
  student_name: StudentNameSchema,
  figure_id: FigureIdSchema,
  palette_id: PaletteIdSchema,
  position_id: PositionIdSchema,
  rationale: z
    .string()
    .trim()
    .max(500, "La justificación no puede exceder 500 caracteres")
    .optional()
    .default(""),
  file: z.any().optional(),
});
