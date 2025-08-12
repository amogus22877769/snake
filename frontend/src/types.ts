import type z from "zod";
import type {
  AppleSchema,
  BlockSchema,
  ConfigSchema,
  DirectionSchema,
  NewDirectionSchema,
  SnakeSchema,
  SnapshotSchema,
} from "./zodSchemas";

type DirectionType = z.infer<typeof DirectionSchema>;

type AppleType = z.infer<typeof AppleSchema>;

type BlockType = z.infer<typeof BlockSchema>;

type SnakeType = z.infer<typeof SnakeSchema>;

type SnapshotType = z.infer<typeof SnapshotSchema>;

type NewDirectionType = z.infer<typeof NewDirectionSchema>;

type ConfigType = z.infer<typeof ConfigSchema>;

export type {
  DirectionType,
  AppleType,
  BlockType,
  SnakeType,
  SnapshotType,
  NewDirectionType,
  ConfigType,
};
