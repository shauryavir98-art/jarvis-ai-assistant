package com.example.alj.config;

import com.example.alj.service.UserService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@RequiredArgsConstructor
@Slf4j
public class DataInitializer {

    @Bean
    CommandLineRunner initDefaultAdmin(UserService userService) {
        return args -> {
            try {
                userService.createAdminIfNotExists("admin", "admin@jarvis.local", "admin123");
                log.info("✅ Default admin user initialized (username: admin, password: admin123)");
            } catch (Exception e) {
                log.warn("⚠️ Could not create default admin user: {}", e.getMessage());
            }
        };
    }
}
