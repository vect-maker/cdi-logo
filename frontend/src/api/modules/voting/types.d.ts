import type { z } from "zod";
import type {
  FigureIdSchema,
  PaletteIdSchema,
  PositionIdSchema,
  StudentIdSchema,
  StudentNameSchema,
} from "./domain";
import type {
  CheckStudentRequestSchema,
  SubmitVoteRequestSchema,
} from "./requests";
import type {
  CheckStudentResponseSchema,
  VoteReceiptResponseSchema,
  VotingStatsResponseSchema,
} from "./responses";

export type FigureId = z.infer<typeof FigureIdSchema>;
export type PaletteId = z.infer<typeof PaletteIdSchema>;
export type PositionId = z.infer<typeof PositionIdSchema>;
export type StudentId = z.infer<typeof StudentIdSchema>;
export type StudentName = z.infer<typeof StudentNameSchema>;

export type CheckStudentRequest = z.infer<typeof CheckStudentRequestSchema>;
export type SubmitVoteRequest = z.infer<typeof SubmitVoteRequestSchema>;

export type CheckStudentResponse = z.infer<typeof CheckStudentResponseSchema>;
export type VoteReceiptResponse = z.infer<typeof VoteReceiptResponseSchema>;
export type VotingStatsResponse = z.infer<typeof VotingStatsResponseSchema>;
