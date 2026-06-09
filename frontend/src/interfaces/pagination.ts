export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface PaginationFilters {
  page?: number;
  page_size?: number;
  search?: string;
}
