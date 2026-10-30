import { z } from "zod";

export const ErrorPayloadSchema = z.object({
  message: z.string().default("Ocurrió un error inesperado"),
  detail: z.union([z.string(), z.array(z.any()), z.record(z.string(), z.any())]).optional(),
  code: z.string().optional(),
});
