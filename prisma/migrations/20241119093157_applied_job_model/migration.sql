/*
  Warnings:

  - You are about to drop the `_UserJobs` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "_UserJobs" DROP CONSTRAINT "_UserJobs_A_fkey";

-- DropForeignKey
ALTER TABLE "_UserJobs" DROP CONSTRAINT "_UserJobs_B_fkey";

-- AlterTable
ALTER TABLE "User" ADD COLUMN     "bookmarked_jobs" TEXT[];

-- DropTable
DROP TABLE "_UserJobs";

-- CreateTable
CREATE TABLE "Applied_Jobs" (
    "id" UUID NOT NULL,
    "jobId" UUID NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'applied',
    "userId" UUID NOT NULL,

    CONSTRAINT "Applied_Jobs_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Applied_Jobs_jobId_userId_key" ON "Applied_Jobs"("jobId", "userId");

-- AddForeignKey
ALTER TABLE "Applied_Jobs" ADD CONSTRAINT "Applied_Jobs_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
