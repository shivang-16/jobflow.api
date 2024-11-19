/*
  Warnings:

  - You are about to drop the column `userId` on the `Job` table. All the data in the column will be lost.

*/
-- DropForeignKey
ALTER TABLE "Job" DROP CONSTRAINT "Job_userId_fkey";

-- AlterTable
ALTER TABLE "Job" DROP COLUMN "userId";

-- CreateTable
CREATE TABLE "_UserJobs" (
    "A" UUID NOT NULL,
    "B" UUID NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "_UserJobs_AB_unique" ON "_UserJobs"("A", "B");

-- CreateIndex
CREATE INDEX "_UserJobs_B_index" ON "_UserJobs"("B");

-- AddForeignKey
ALTER TABLE "_UserJobs" ADD CONSTRAINT "_UserJobs_A_fkey" FOREIGN KEY ("A") REFERENCES "Job"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_UserJobs" ADD CONSTRAINT "_UserJobs_B_fkey" FOREIGN KEY ("B") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;
