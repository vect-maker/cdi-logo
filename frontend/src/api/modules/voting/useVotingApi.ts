import { useApiFetch } from "../../useApiFetch";
import { CheckStudentRequestSchema, SubmitVoteRequestSchema } from "./requests";
import {
  CheckStudentResponseSchema,
  VoteReceiptResponseSchema,
  VotingStatsResponseSchema,
} from "./responses";
import type {
  CheckStudentRequest,
  CheckStudentResponse,
  SubmitVoteRequest,
  VoteReceiptResponse,
  VotingStatsResponse,
} from "./types";

export const useVotingApi = () => {
  /**
   * Check if a student has already voted in Round 1.
   * GET /api/v1/votes/check/{student_id}
   */
  async function checkStudent(payload: CheckStudentRequest): Promise<CheckStudentResponse> {
    const validated = CheckStudentRequestSchema.parse(payload);
    const { data, error } = await useApiFetch(
      `/api/v1/votes/check/${encodeURIComponent(validated.student_id)}`
    )
      .get()
      .json();

    if (error.value || !data.value) {
      throw error.value ?? new Error("No se pudo verificar el estado del carné");
    }
    return CheckStudentResponseSchema.parse(data.value);
  }

  /**
   * Submit a student vote with validation (supports JSON or multipart if file is attached).
   * POST /api/v1/votes
   */
  async function submitVote(payload: SubmitVoteRequest): Promise<VoteReceiptResponse> {
    const validatedPayload = SubmitVoteRequestSchema.parse(payload);

    let bodyData: unknown = validatedPayload;
    if (validatedPayload.file) {
      const formData = new FormData();
      formData.append("student_id", validatedPayload.student_id);
      formData.append("student_name", validatedPayload.student_name);
      formData.append("figure_id", validatedPayload.figure_id);
      formData.append("palette_id", validatedPayload.palette_id);
      formData.append("position_id", validatedPayload.position_id);
      formData.append("rationale", validatedPayload.rationale || "");
      formData.append("file", validatedPayload.file);
      bodyData = formData;
    }

    const { data, error } = await useApiFetch("/api/v1/votes")
      .post(bodyData)
      .json();

    if (error.value || !data.value) {
      throw error.value ?? new Error("Error al registrar el voto");
    }
    return VoteReceiptResponseSchema.parse(data.value);
  }

  /**
   * Fetch current voting statistics.
   * GET /api/v1/votes/stats
   */
  async function getStats(): Promise<VotingStatsResponse> {
    const { data, error } = await useApiFetch("/api/v1/votes/stats").get().json();
    if (error.value || !data.value) {
      throw error.value ?? new Error("No se pudieron cargar las estadísticas");
    }
    return VotingStatsResponseSchema.parse(data.value);
  }

  return {
    checkStudent,
    submitVote,
    getStats,
  };
};
