"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Plus } from "lucide-react";
import { AxiosError } from "axios";
import { toast } from "sonner";
import { useCreateProject } from "@/hooks/use-projects";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from "@/components/ui/dialog";

const schema = z.object({
  name: z.string().min(1, "Name is required"),
  description: z.string().optional(),
  target_url: z.string().url("Enter a valid URL (https://...)"),
});

type FormValues = z.infer<typeof schema>;

export function CreateProjectDialog() {
  const [open, setOpen] = useState(false);
  const createProject = useCreateProject();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<FormValues>({ resolver: zodResolver(schema) });

  async function onSubmit(values: FormValues) {
    try {
      await createProject.mutateAsync(values);
      toast.success("Project created");
      reset();
      setOpen(false);
    } catch (err) {
      const message =
        err instanceof AxiosError
          ? err.response?.data?.detail ?? "Failed to create project"
          : "Failed to create project";
      toast.error(message);
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Project
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create Project</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input id="name" placeholder="My Web App" {...register("name")} />
            {errors.name && <p className="text-sm text-destructive">{errors.name.message}</p>}
          </div>
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Input id="description" placeholder="Optional" {...register("description")} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="target_url">Target URL</Label>
            <Input id="target_url" placeholder="https://example.com" {...register("target_url")} />
            {errors.target_url && (
              <p className="text-sm text-destructive">{errors.target_url.message}</p>
            )}
          </div>
          <DialogFooter>
            <Button type="submit" disabled={createProject.isPending}>
              {createProject.isPending ? "Creating..." : "Create"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
