export interface SummaryResponse {
    details: {
        email?: string[];
        full_name?: string[];
        skills: string[];
        experience: string[];
        languages_spoken: string[];
        phone_number: string[];
        education: string[];
    };
    experience_level: string;
}
