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
      // return true;
      console.log(val.blocks);
      let prevBlock = val.blocks[0];
      if (new Set(val.blocks).size != val.blocks.length) {
        return false;
      }
      for (const block of val.blocks.slice(1)) {
        console.log(block, prevBlock);
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

const SnapshotSchema = z.object({
  snakes: z.array(SnakeSchema),
  apples: z.array(AppleSchema),
});

const NewDirectionSchema = z.object({
  name: SnakeNameSchema,
  direction: DirectionSchema,
});

export {
  DirectionSchema,
  BlockSchema,
  AppleSchema,
  SnakeSchema,
  SnapshotSchema,
  NewDirectionSchema,
};
