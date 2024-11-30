/*
  Warnings:

  - You are about to drop the column `status` on the `User` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "User" DROP COLUMN "status",
ADD COLUMN     "job_statuses" TEXT[] DEFAULT ARRAY['bookmarked', 'applied', 'accepted', 'rejected']::TEXT[];
