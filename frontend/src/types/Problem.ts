export interface Problem {
    id: number;
    number: number;
    name: string;
    description: string;
    difficulty: 'Easy' | 'Medium' | 'Hard';
    category: string;
    solution: string;
    approach: string;
    timeComplexity: string;
    spaceComplexity: string;
    dateSolved: string;
    status: 'Solved' | 'In Progress' | 'Not Started';
    notes?: string;
} 