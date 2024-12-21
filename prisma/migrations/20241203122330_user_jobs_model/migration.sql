-- CreateTable
CREATE TABLE "User_Jobs" (
    "id" UUID NOT NULL,
    "title" TEXT NOT NULL,
    "job_link" TEXT,
    "job_type" TEXT,
    "apply_link" TEXT,
    "job_location" TEXT,
    "job_salary" TEXT,
    "job_description" TEXT,
    "skills_required" TEXT,
    "source" TEXT,
    "source_logo" TEXT,
    "posted" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,
    "userId" UUID NOT NULL,
    "companyId" UUID,

    CONSTRAINT "User_Jobs_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_Jobs_title_companyId_key" ON "User_Jobs"("title", "companyId");

-- AddForeignKey
ALTER TABLE "User_Jobs" ADD CONSTRAINT "User_Jobs_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "User_Jobs" ADD CONSTRAINT "User_Jobs_companyId_fkey" FOREIGN KEY ("companyId") REFERENCES "Company"("id") ON DELETE SET NULL ON UPDATE CASCADE;
