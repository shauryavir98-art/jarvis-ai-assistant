package com.example.alj.service;

import com.example.alj.dto.UserRegistrationDto;
import com.example.alj.entity.Role;
import com.example.alj.entity.User;
import com.example.alj.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    public User registerUser(UserRegistrationDto dto) {
        if (userRepository.existsByUsername(dto.getUsername())) {
            throw new RuntimeException("Username '" + dto.getUsername() + "' is already taken");
        }
        if (userRepository.existsByEmail(dto.getEmail())) {
            throw new RuntimeException("Email '" + dto.getEmail() + "' is already registered");
        }
        if (!dto.getPassword().equals(dto.getConfirmPassword())) {
            throw new RuntimeException("Passwords do not match");
        }

        User user = User.builder()
                .username(dto.getUsername())
                .email(dto.getEmail())
                .password(passwordEncoder.encode(dto.getPassword()))
                .role(Role.ROLE_USER)
                .build();

        return userRepository.save(user);
    }

    @Transactional
    public User createAdminIfNotExists(String username, String email, String rawPassword) {
        if (userRepository.existsByUsername(username)) {
            return userRepository.findByUsername(username).orElseThrow();
        }

        User admin = User.builder()
                .username(username)
                .email(email)
                .password(passwordEncoder.encode(rawPassword))
                .role(Role.ROLE_ADMIN)
                .build();

        return userRepository.save(admin);
    }

    public Optional<User> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }

    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }

    public long getUserCount() {
        return userRepository.count();
    }
}
