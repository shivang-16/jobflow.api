/*
  Warnings:

  - You are about to drop the `Applied_Jobs` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "Applied_Jobs" DROP CONSTRAINT "Applied_Jobs_jobId_fkey";

-- DropForeignKey
ALTER TABLE "Applied_Jobs" DROP CONSTRAINT "Applied_Jobs_userId_fkey";

-- AlterTable
ALTER TABLE "Job" ALTER COLUMN "posted" SET DEFAULT CURRENT_TIMESTAMP;

-- DropTable
DROP TABLE "Applied_Jobs";

-- DropEnum
DROP TYPE "UserStatus";

-- CreateTable
CREATE TABLE "Tracked_Jobs" (
    "id" UUID NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'applied',
    "userId" UUID NOT NULL,
    "jobId" UUID NOT NULL,

    CONSTRAINT "Tracked_Jobs_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Tracked_Jobs_jobId_userId_key" ON "Tracked_Jobs"("jobId", "userId");

-- AddForeignKey
ALTER TABLE "Tracked_Jobs" ADD CONSTRAINT "Tracked_Jobs_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Tracked_Jobs" ADD CONSTRAINT "Tracked_Jobs_jobId_fkey" FOREIGN KEY ("jobId") REFERENCES "Job"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
