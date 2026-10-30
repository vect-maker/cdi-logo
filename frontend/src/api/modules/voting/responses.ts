import { z } from "zod";
import {
  FigureIdSchema,
  PaletteIdSchema,
  PositionIdSchema,
  StudentIdSchema,
} from "./domain";

export const CheckStudentResponseSchema = z.object({
  student_id: StudentIdSchema,
  has_voted: z.boolean(),
  message: z.string().optional(),
});

export const VoteReceiptResponseSchema = z.object({
  receipt_id: z.string(),
  student_id: StudentIdSchema,
  student_name: z.string(),
  figure_id: FigureIdSchema,
  palette_id: PaletteIdSchema,
  position_id: PositionIdSchema,
  timestamp: z.string(),
  round: z.number().int().default(1),
  verification_hash: z.string(),
  has_attachment: z.boolean().default(false),
  attachment_filename: z.string().nullable().optional(),
});

export const VotingStatsResponseSchema = z.object({
  total_votes: z.number().int().nonnegative(),
  round: z.number().int().default(1),
  by_figure: z.record(z.string(), z.number().int().nonnegative()),
});
