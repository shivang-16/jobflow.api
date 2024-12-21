/*
  Warnings:

  - A unique constraint covering the columns `[title,companyId,userId]` on the table `User_Jobs` will be added. If there are existing duplicate values, this will fail.

*/
-- DropIndex
DROP INDEX "User_Jobs_title_companyId_key";

-- AlterTable
ALTER TABLE "User_Jobs" ADD COLUMN     "status" TEXT NOT NULL DEFAULT 'applied';

-- CreateIndex
CREATE UNIQUE INDEX "User_Jobs_title_companyId_userId_key" ON "User_Jobs"("title", "companyId", "userId");
