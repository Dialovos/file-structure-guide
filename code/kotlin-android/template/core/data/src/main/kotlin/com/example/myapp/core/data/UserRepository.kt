package com.example.myapp.core.data

/**
 * Sample repository sitting in `core:data`. Repositories own the
 * mapping between remote/local sources and domain models exposed to
 * `feature:*` modules. Keep methods suspend / Flow-returning to make
 * them easy to test without Robolectric.
 */
class UserRepository {
    suspend fun loadUserName(userId: String): String {
        // In a real implementation this would call a Retrofit service
        // from :core:network and a Room DAO from :core:database.
        return "user-$userId"
    }
}
