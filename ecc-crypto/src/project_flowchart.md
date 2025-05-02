```mermaid
graph TD
    subgraph Common Setup
        A[Define/Agree on ECC Domain Parameters: E, G, n, p]
    end

    subgraph Key Generation User A
        B[Choose Random Private Key: Xa E Z; 1 < Xa < n] --> C{Calculate Public Key: Ya = Xa * G}
        C --> D["Public Key: Ya, Private Key: Xa (Secret)"]
    end
    subgraph Key Generation User B
        E[Choose Random Private Key: Xb e Z; 1 < Xb < n] --> F{Calculate Public Key: Yb = Xb * G}
        F --> G["Public Key: Yb, Private Key: Xb (Secret)"]
    end

    A --> B
    A --> E

    D --> H{Select Use Case}
    G --> H

    subgraph Case 1: Digital Signature
        direction LR
        H --> S1["User A (Signer): Wants to sign Message m"]
        S1 --> S2[User A: Calculate Hash m = e]
        S2 --> S3[User A: Generate random ephemeral key k, 1 < k < n]
        S3 --> S4[User A: Calculate Point R = k * G]
        S4 --> S5[User A: Get x-coordinate of R -> r = R.x mod n]
        S5 --> S6{If r == 0, go back to S3}
        S6 -- No --> S7["User A: Calculate s = k^-1 * (e + r * Xa) mod n"]
        S7 --> S8{If s == 0, go back to S3}
        S8 -- No --> S9[User A: Signature r, s]
        S9 --> V1["User B (Verifier): Receives Message m and Signature r, s"]
        V1 --> V2[User B: Has User A's Public Key Ya]
        V2 --> V3[User B: Verify r and s are in range 1 to n-1]
        V3 -- Yes --> V4[User B: Calculate Hash m = e]
        V4 --> V5[User B: Calculate w = s^-1 mod n]
        V5 --> V6[User B: Calculate u1 = e * w mod n]
        V6 --> V7[User B: Calculate u2 = r * w mod n]
        V7 --> V8[User B: Calculate Point P = u1 * G + u2 * Ya]
        V8 --> V9{If P is point at infinity, Signature Invalid}
        V9 -- No --> V10[User B: Get x-coordinate of P -> v = P.x mod n]
        V10 --> V11{Is v == r?}
        V11 -- Yes --> V12[Signature Valid]
        V11 -- No --> V13[Signature Invalid]
        V3 -- No --> V13
    end

    subgraph Case 2: Key Exchange
        direction TB
        H --> K1[User A and User B agree on Domain Parameters]
        K1 --> K2[User A: Has Key Pair Xa, Ya]
        K1 --> K3[User B: Has Key Pair Xb, Yb]
        K2 --> K4[Exchange Public Keys: User A sends Ya to User B, User B sends Yb to User A]
        K3 --> K4
        K4 --> K5[User A: Calculate Shared Secret Point S = Xa * Yb]
        K4 --> K6[User B: Calculate Shared Secret Point S = Xb * Ya]
        K5 --> K7{Result S = Xa * Xb * G = Xb * Xa * G}
        K6 --> K7
        K7 --> K8[Derive Shared Symmetric Key K from S]
        K8 --> K9[Shared Secret Key K, Used for subsequent symmetric encryption]
    end

    subgraph Case 3: Encrypt Decrypt
        direction LR
        H --> E1["User A (Sender): Wants to encrypt Message m for User B"]
        E1 --> E2[User A: Has User B's Public Key Yb]
        E2 --> E3[User A: Generate ephemeral ECC key pair r, R = r * G]
        E3 --> E4[User A: Derive Shared Secret S = r * Yb]
        E4 --> E5[User A: Use KDF on S.x to generate Symmetric Keys k_E for encryption, k_M for MAC]
        E5 --> E6["User A: Encrypt Message: c = Encrypt_kE(m)"]
        E6 --> E7["User A: Calculate MAC: tag = MAC_kM(c)"]
        E7 --> E8[User A: Send Ciphertext Bundle R, c, tag to User B]

        E8 --> D1["User B (Receiver): Receives R, c, tag"]
        D1 --> D2[User B: Has own Private Key Xb]
        D2 --> D3[User B: Derive Shared Secret S = Xb * R]
        D3 --> D4["User B: Use KDF on S.x to generate Symmetric Keys k_E, k_M (Same as User A's)"]
        D4 --> D5["User B: Calculate MAC: tag' = MAC_kM(c)"]
        D5 --> D6{Is tag' == tag?}
        D6 -- Yes --> D7["User B: Decrypt Ciphertext: m = Decrypt_kE(c)"]
        D7 --> D8[Decrypted Message m]
        D6 -- No --> D9[Decryption Failed, MAC Invalid]
    end