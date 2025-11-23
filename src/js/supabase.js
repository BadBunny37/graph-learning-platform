import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://ohhdqlciitoihqzyxqcn.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9oaGRxbGNpaXRvaWhxenl4cWNuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NTcyNjUsImV4cCI6MjA3OTQzMzI2NX0.s1mTR-UFVULzbh1d_Z_LMNqFxbYH04OfFzPIBDHa-mM'

export const supabase = createClient(supabaseUrl, supabaseKey)

// Auth Helpers
export async function signUp(email, password, fullName) {
    const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
            data: {
                full_name: fullName,
                avatar_url: `https://ui-avatars.com/api/?name=${encodeURIComponent(fullName)}&background=random`
            }
        }
    })
    return { data, error }
}

export async function signIn(email, password) {
    const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
    })
    return { data, error }
}

export async function signOut() {
    const { error } = await supabase.auth.signOut()
    return { error }
}

export async function getCurrentUser() {
    const { data: { user } } = await supabase.auth.getUser()
    return user
}

export async function getProfile(userId) {
    const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', userId)
        .single()
    return { data, error }
}
