import type { z } from "zod";
import type { ErrorPayloadSchema } from "./schemas";

export type ErrorPayload = z.infer<typeof ErrorPayloadSchema>;
