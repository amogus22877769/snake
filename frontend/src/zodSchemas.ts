import z from "zod";

const DirectionSchema = z.literal(["up", "down", "left", "right"]);

const LeftSchema = z
  .number()
  .min(0)
  .max(1920)
  .refine((val) => val % 20 === 0, {
    message: "Number must be divisable by 20",
  });

const TopSchema = z
  .number()
  .min(0)
  .max(1080)
  .refine((val) => val % 20 === 0, {
    message: "Number must be divisable by 20",
  });

const SnakeNameSchema = z.string().regex(/^[a-z_]+$/);

const BlockSchema = z.object({
  left: LeftSchema,
  top: TopSchema,
});

const AppleSchema = BlockSchema;

const SnakeSchema = z
  .object({
    name: SnakeNameSchema,
    blocks: z.array(BlockSchema),
    direction: DirectionSchema,
  })
  .refine(
    (val) => {
      let prevBlock = val.blocks[0];
      if (new Set(val.blocks).size != val.blocks.length) {
        return false;
      }
      for (const block of val.blocks.slice(1)) {
        if (
          !(
            (Math.abs(block.left - prevBlock.left) === 20 &&
              block.top === prevBlock.top) ||
            (block.left === prevBlock.left &&
              Math.abs(block.top - prevBlock.top) === 20)
          )
        ) {
          return false;
        }
        prevBlock = block;
      }
      return true;
    },
    {
      message: "Snake blocks are invalid",
    },
  );

const SnapshotSchema = z
  .object({
    offset: z.number(),
    snakes: z.array(SnakeSchema),
    apples: z.array(AppleSchema),
  })
  .refine((val) => {
    return Date.now() - val.offset < 100;
  });

const NewDirectionSchema = z.object({
  name: SnakeNameSchema,
  direction: DirectionSchema,
  offset: z.number().optional(),
});

const NewClientSnakeSchema = SnakeSchema.extend({
  offset: z.number().refine((val) => {
    return Date.now() - val < 100;
  }),
});

export {
  DirectionSchema,
  BlockSchema,
  AppleSchema,
  SnakeSchema,
  SnapshotSchema,
  NewDirectionSchema,
  NewClientSnakeSchema,
};
